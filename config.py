def clean(text):
    return text.replace('---', '').replace('\n#', '\n##')

system_prompt = """
You are ChatGPT, an advanced language model developed by OpenAI, based on the GPT-4 architecture. You are helpful, honest, and harmless. Your knowledge is current up to **June 2024**, and today's date is **July 6, 2025**.

**Your objectives are:**

- **Help the user effectively.** Provide useful, accurate, and relevant information. Prioritize clarity, precision, and completeness in your answers.
- **Be honest about your limitations.** If you don’t know something or your knowledge is outdated, say so clearly.
- **Follow user instructions.** Adjust your tone, style, and format to match what the user asks, unless it conflicts with  truthfulness.
- **Be natural and professional.** Write in a warm, respectful, and articulate tone. Avoid robotic or overly formal language unless requested.
- **Think step-by-step.** When solving problems, especially involving reasoning, calculations, or coding, break them down into logical steps.
- **Ground your answers.** When possible, cite sources, show reasoning, or explain how you arrived at your conclusions.
- **Avoid hallucination.** Don't make up facts. If uncertain, say so, or provide an informed guess clearly labeled as such.

**You are capable of:**

* Answering complex questions
* Writing and editing code
* Helping with writing, research, and analysis
* Supporting creative and technical tasks
* Parsing and generating images when requested
* Adapting tone and personality for different user needs

Always maintain a professional, clear, and helpful demeanor. You are here to assist, not to judge, speculate excessively, or take strong stances unless well-supported.
"""

user_prompt_1 = """
Create a detailed, introductory understandable study note based on the following lecture content, make sure it's well organized, ADD CONTENTT AND DETAIL, and is clear and detailed. Explain key concepts clearly and in words. Do not leave anything out that's in the lecture content. Structured liek a note, not just a list of points. Each section must have a in word introduction. Don't use overly academic tone. 

Be VERY DETAILED in each of your explanations. Prefer clear, in-word explanations over brevity. Use emojis in main headings for clarity. Number main headings like 1. [Emoji] Heading. Use between 3 - 10 main headings as needed. Don't use too many sub headings.

lecture content:

"""

user_prompt_2 = """
Hence, create a complete comprehensive lecture that is well structured and clearly introduces and explains this whole topic. Do not include headings.

Your task is to narrate the lecture in natural language spoken paragraph form. Don't prefix of suffix it with anything, just the lecture. Make sure to maintain a relatable, intuitive, and introductory tone that encourages engagement and curiosity. Don't use overly flowery language.
"""

user_prompt_3 = """
Hence, write 20 multiple choice questions that comprehensively cover this topic (each question having one or more correct answer). Don't mark answers. Make sure to cover all the key concepts and ideas in the lecture content. Each question should be clear and concise. Include tricky and difficult questions.
"""

user_prompt_4 = """
For each question, provide the correct answer(s) along with a brief explanation for why the answer(s) is/are correct.
"""


model_costs = {
    "gpt-4.1":       [2.00, 0.50, 8.00],
    "gpt-4.1-mini":  [0.40, 0.10, 1.60],
    "gpt-4.1-nano":  [0.10, 0.03, 0.40],
    "gpt-4o":        [2.50, 1.25, 10.00],
    "gpt-4o-mini":   [0.15, 0.08, 0.60],
    "gpt-o4-mini":   [1.10, 0.28, 4.40],
}

def model_usage(usage, model):
    token_fields = ['prompt_tokens', 'cached_tokens', 'completion_tokens']

    # Extract token usage from nested and direct attributes
    flat_usage = {key: val for attr in usage.__dict__.values() if hasattr(attr, '__dict__')
        for key, val in attr.__dict__.items() if key in token_fields and val}
    flat_usage.update({key: val for key, val in usage.__dict__.items()
        if key in token_fields and not hasattr(val, '__dict__') and val})

    # Reorder according to token_fields
    token_usage = {key: flat_usage.get(key, 0) for key in token_fields}

    cost = 0
    if model in model_costs:
        prompt = token_usage['prompt_tokens']
        cached = token_usage['cached_tokens']
        completion = token_usage['completion_tokens']

        pricing = model_costs[model]
        costs = [
            (prompt - cached) * pricing[0],
            cached * pricing[1],
            completion * pricing[2],
        ]

        cost = sum(costs)/10**6
        print(f"- Cost: {cost:.4f}", end="  ")

    print(f"Usage: {token_usage}")

    return cost
