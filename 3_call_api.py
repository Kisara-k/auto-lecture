import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from openai import OpenAI

from config import system_prompt, user_prompt_1, user_prompt_2, user_prompt_3, user_prompt_4, user_prompt_5, clean, model_usage
from config import MODEL, START, NUM_LECS, GET_TRANSCRIPTS, GET_KEY_POINTS, GET_Q_AND_A, TRY_REUSE_NOTES

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
os.makedirs("outputs/json", exist_ok=True)

def load_data(name):
    data_path = os.path.join("outputs/json", f"{name}.json")
    data_dict = {}

    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            data_dict = {item["index"]: {k: item[k] for k in ["title", "content"]}
                for item in existing_data}

    return data_dict, data_path, threading.Lock()

transcripts, transcripts_path, transcripts_lock = load_data("transcripts")
study_notes, study_notes_path, study_notes_lock = load_data("study_notes")
key_points, key_points_path, key_points_lock = load_data("key_points")
questions, questions_path, questions_lock = load_data("questions")
answers, answers_path, answers_lock = load_data("answers")

def process_lecture(lecture):
    id = lecture['index']
    title = lecture['title']
    content = lecture['content']

    if not (START <= id < START + NUM_LECS):
        return

    print(f"Processing {id}: {title}")

    lec_prompt_1 = user_prompt_1 + title + "\n\n" + content

    # Step 1
    
    text_1 = None
    if TRY_REUSE_NOTES:
        with study_notes_lock:
            text_1 = study_notes.get(id, {}).get("content")
    
    if text_1 is None:
        text_1, _ = generate([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": lec_prompt_1}
            ], model='gpt-4.1-mini')
        
        with study_notes_lock:
            study_notes[id] = {"title": title, "content": text_1}

    # Step 2

    results = {}
    results_lock = threading.Lock()

    def add_to_results(key, source_dict, source_lock):
        with source_lock:
            item = source_dict.get(id, {}).get("content")
        if item is not None:
            with results_lock:
                results[key] = item

    def step_2a():

        if GET_TRANSCRIPTS:
        
            text_2, _ = generate([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": lec_prompt_1},
                {"role": "assistant", "content": text_1},
                {"role": "user", "content": user_prompt_2},])

            with transcripts_lock:
                transcripts[id] = {"title": title, "content": text_2}

    def step_2b():
        
        if GET_Q_AND_A:
        
            text_3, _ = generate([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": lec_prompt_1},
                {"role": "assistant", "content": text_1},
                {"role": "user", "content": user_prompt_3},])
            
            with questions_lock:
                questions[id] = {"title": title, "content": text_3}
            
            text_4, _ = generate([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": lec_prompt_1},
                {"role": "assistant", "content": text_1},
                {"role": "user", "content": user_prompt_3},
                {"role": "assistant", "content": text_3},
                {"role": "user", "content": user_prompt_4},])
            
            with answers_lock:
                answers[id] = {"title": title, "content": text_4}
        
        add_to_results("text_3", questions, questions_lock)
        add_to_results("text_4", answers, answers_lock)
    
    def step_2c():
        
        if GET_KEY_POINTS:
        
            text_5, _ = generate([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": lec_prompt_1},
                {"role": "assistant", "content": text_1},
                {"role": "user", "content": user_prompt_5},
                ], model='gpt-4.1-mini')
            
            with key_points_lock:
                key_points[id] = {"title": title, "content": text_5}
        
        add_to_results("text_5", key_points, key_points_lock)

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

# Save Output JSONs

def save_data(data_dict, file_path):
    data_list = [
        {"index": id, "title": data["title"], "content": data["content"]}
        for id, data in sorted(data_dict.items())
    ]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

save_data(transcripts, transcripts_path)
save_data(study_notes, study_notes_path)
save_data(key_points, key_points_path)
save_data(questions, questions_path)
save_data(answers, answers_path)

print("\nLecture Processing Complete'")
print(f"Total API Cost: {total_cost:.4f}")
