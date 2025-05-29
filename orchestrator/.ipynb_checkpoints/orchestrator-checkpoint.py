from openai import OpenAI
from .prompts import ORCHESTRATOR_SYS_PROMPT, FINAL_SYS_PROMPT
import requests
import json
import os

api_key = os.getenv("TOGETHER_API")
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")


def get_orchertration_resposne(query, history):

    history = history[::-1][:5]
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[
            {
                "role": "system",
                "content": ORCHESTRATOR_SYS_PROMPT,
            },
            *history,
            {"role": "user", "content": "Query: " + query},
        ],
    )
    r = response.choices[0].message.content
    data = json.loads(str(r))

    if data["tool"] == "get_change":
        result = requests.post(
            url="http://127.0.0.1:7860/data/get_historical_data",
            json=data["parameters"],
        ).json()

    elif data["tool"] == "get_earning":
        result = requests.post(
            url="http://127.0.0.1:7860/data/get_earning_metrics",
            json=data["parameters"],
        ).json()

    elif data["tool"] == "get_portfolio_status":
        result = requests.post(
            url="http://127.0.0.1:7860/data/get_portfolio_data", json=data["parameters"]
        ).json()

    elif data["tool"] == "get_knowledge":
        result = requests.post(
            url="http://127.0.0.1:7860/data/get_knowledge", json=data["parameters"]
        ).json()

    elif data["tool"] == None:
        return data["parameters"]

    else:
        result = {
            "response": "An error occured internally please communicate this to user firmly"
        }
    return result


def final_response(query, context, history):

    history = history[::-1][:5]
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[
            {
                "role": "system",
                "content": FINAL_SYS_PROMPT,
            },
            *history,
            {"role": "user", "content": f"Query : {query} \n\n Context: {context}"},
        ],
        stream=True,
    )

    for chunk in response:
        yield chunk.choices[0].delta.content or ""
