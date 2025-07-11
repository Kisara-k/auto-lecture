import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from openai import OpenAI

from config import system_prompt, user_prompt_1, user_prompt_2, user_prompt_3, user_prompt_4, user_prompt_5, clean, model_usage
from config import MODEL, START, NUM_LECS, GET_TRANSCRIPTS, GET_KEY_POINTS, GET_Q_AND_A

load_dotenv()
openai_key = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=openai_key)

total_cost = 0.0
cost_lock = threading.Lock()

def generate(messages, model=MODEL):
    start = time.time()
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,  # Adjust for more creative or deterministic output
        max_tokens=10000,  # Increase this if responses are getting cut off
        top_p=0.3,
        frequency_penalty=0,
        presence_penalty=0
    )

    elapsed = time.time() - start
    print(f"Completion took {elapsed:.2f} seconds")
    
    try:
        cost = model_usage(completion.usage, model)
    except Exception as e:
        print(f"Error getting model usage: {e}")
        cost = 0

    with cost_lock:
        global total_cost
        total_cost += cost

    return completion.choices[0].message.content, completion

import json

with open('Lectures.json', 'r', encoding='utf-8') as f:
    lectures = json.load(f)


os.makedirs("outputs", exist_ok=True)
transcripts = {}
transcripts_path = os.path.join("outputs", "transcripts.json")

if os.path.exists(transcripts_path):
    with open(transcripts_path, "r", encoding="utf-8") as f:
        existing_transcripts = json.load(f)
        transcripts = {item["index"]: {"title": item["title"], "content": item["content"]} for item in existing_transcripts}

transcripts_lock = threading.Lock()

def process_lecture(lecture):
    id = lecture['index']
    title = lecture['title']
    content = lecture['content']

    if not (START <= id < START + NUM_LECS):
        return

    print(f"Processing {id}: {title}")

    lec_prompt_1 = user_prompt_1 + title + "\n\n" + content

    # Step 1

    text_1, _ = generate([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": lec_prompt_1}
        ], model='gpt-4.1-mini')

    results = {}

    def step_2a():

        if not GET_TRANSCRIPTS:
            return
        
        text_2, _ = generate([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": lec_prompt_1},
            {"role": "assistant", "content": text_1},
            {"role": "user", "content": user_prompt_2},
        ])
        with transcripts_lock:
            transcripts[id] = {
                "title": title,
                "content": text_2,
            }

    def step_2b():
        
        if not GET_Q_AND_A:
            return
        
        text_3, _ = generate([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": lec_prompt_1},
            {"role": "assistant", "content": text_1},
            {"role": "user", "content": user_prompt_3},])

        results["text_3"] = text_3
        
        text_4, _ = generate([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": lec_prompt_1},
            {"role": "assistant", "content": text_1},
            {"role": "user", "content": user_prompt_3},
            {"role": "assistant", "content": text_3},
            {"role": "user", "content": user_prompt_4},])

        results["text_4"] = text_4
    
    def step_2c():
        
        if not GET_KEY_POINTS:
            return
        
        text_5, _ = generate([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": lec_prompt_1},
            {"role": "assistant", "content": text_1},
            {"role": "user", "content": user_prompt_5},
            ], model='gpt-4.1-mini')
        
        results["text_5"] = text_5

    threads = [
        threading.Thread(target=step_2a),
        threading.Thread(target=step_2b),
        threading.Thread(target=step_2c),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    filepath = os.path.join("outputs", f"{id:02d} {re.sub(r'[<>:"/\\|?*]', '', title)}.md")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("## " + title + "\n\n")
        if "text_5" in results:
            f.write("\n\n" + "### " + "Key Points" + "\n\n")
            f.write(clean(results["text_5"]))
        f.write("\n\n<br>\n\n" + "## " + "Study Notes" + "\n\n")
        f.write(clean(text_1))
        if "text_3" in results:
            f.write("\n\n<br>\n\n" + "## " + "Questions" + "\n\n")
            f.write(clean(results["text_3"]))
        if "text_4" in results:
            f.write("\n\n<br>\n\n" + "## " + "Answers" + "\n\n")
            f.write(clean(results["text_4"]))


with ThreadPoolExecutor() as executor:
    executor.map(process_lecture, lectures)

# Save Transcripts

transcripts_list = [
    {"index": lecture_id, "title": transcript["title"], "content": transcript["content"]}
    for lecture_id, transcript in sorted(transcripts.items())
]
with open(transcripts_path, "w", encoding="utf-8") as f:
    json.dump(transcripts_list, f, ensure_ascii=False, indent=2)

print("\nLecture Processing Complete'")
print(f"Total API Cost: {total_cost:.4f}")
