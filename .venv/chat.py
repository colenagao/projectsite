import csv, os
import openai
import sys
from openai import OpenAI


def generate_prompt_from_txt(txt_file):
    with open(txt_file, "r") as file:
        prompt = file.read()
    return prompt


def generate_response(user_input):
    csv_file = "star.txt"
    prompt = generate_prompt_from_txt(csv_file)
    # prompt = prompt + user_input
    # prompt = user_input
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal:evolve1coachv04:9z5AQBc0",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input},
        ],
    )
    return completion.choices[0].message.content


def generate_question(user_input):
    csv_file = "question.txt"
    prompt = generate_prompt_from_txt(csv_file)
    prompt = prompt + user_input
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal:evolve1coachv04:9z5AQBc0",
        messages=[{"role": "system", "content": prompt}],
    )
    return completion.choices[0].message.content