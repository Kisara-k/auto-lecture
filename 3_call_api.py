import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from IPython.display import Markdown, display
from dotenv import load_dotenv
from openai import OpenAI

from config import system_prompt, user_prompt_1, user_prompt_2, user_prompt_3, clean, model_usage

load_dotenv()
openai_key = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=openai_key)

def generate(messages, model='gpt-4.1-mini'):
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
        model_usage(completion.usage, model)
    except Exception as e:
        print(f"Error getting model usage: {e}")

    return completion.choices[0].message.content, completion

import json

with open('Lectures.json', 'r', encoding='utf-8') as f:
    lectures = json.load(f)


os.makedirs("outputs", exist_ok=True)
transcripts = {}
transcripts_lock = threading.Lock()

def process_lecture(lecture):
    id = lecture['index']
    title = lecture['title']
    content = lecture['content']

    print(f"Processing lecture {id}: {title}")

    lec_prompt_1 = user_prompt_1 + title + "\n\n" + content

    # Step 1

    text_1, completion_1 = generate([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": lec_prompt_1}
    ])

    def step_2a():
        
        text_2, completion_2 = generate([
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
        
        text_3, completion_3 = generate([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": lec_prompt_1},
            {"role": "assistant", "content": text_1},
            {"role": "user", "content": user_prompt_3},])
        
        
        filepath = os.path.join("outputs", f"{id:02d} {re.sub(r'[<>:"/\\|?*]', '', title)}.md")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(clean(text_1))
            f.write(clean(text_3))

    thread_a = threading.Thread(target=step_2a)
    thread_b = threading.Thread(target=step_2b)
    thread_a.start()
    thread_b.start()
    thread_a.join()
    thread_b.join()


with ThreadPoolExecutor() as executor:
    executor.map(process_lecture, lectures)

# Save Transcripts

transcripts_list = [
    {"index": lecture_id, "title": transcript["title"], "content": transcript["content"]}
    for lecture_id, transcript in sorted(transcripts.items())
]
with open("outputs/transcripts.json", "w", encoding="utf-8") as f:
    json.dump(transcripts_list, f, ensure_ascii=False, indent=2)

print("Transcripts saved to 'outputs/transcripts.json'")
