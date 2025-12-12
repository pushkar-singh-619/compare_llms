import os
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown,display
load_dotenv(override=True)
try:
    base_url="http://localhost:11434/v1"
    api_key="ollama"

    ollama = OpenAI(base_url=base_url, api_key=api_key)

    MODEL_NAME = "llama3.2"

    print(f"Connecting to local Ollama...{MODEL_NAME}")

    request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
    request += "Answer only with the question, no explanation."

    messages = [{"role":"user", "content":request}]

    response= ollama.chat.completions.create(model=MODEL_NAME,messages=messages)

    question = response.choices[0].message.content
    print(question)

    models = {}
    messages=[{"role":"user", "content":question}]



#ollama
    response= ollama.chat.completions.create(model=MODEL_NAME,messages=messages)
    answer = response.choices[0].message.content

    display(Markdown(answer))
    models[MODEL_NAME] = answer

except Exception as e:
    print(f"Ollama failed: {e}")

try:
#openrouter
    base_url="https://openrouter.ai/api/v1"
    api_key=os.getenv("OPENROUTER_API_KEY")
    openrouter = OpenAI(base_url=base_url,api_key=api_key)

    MODEL_NAME1 = "mistralai/devstral-2512:free"

    print(f"Connecting to openrouter model: {MODEL_NAME1}")

    response = openrouter.chat.completions.create(model=MODEL_NAME1,messages=messages)

    answer1= response.choices[0].message.content
    display(Markdown(answer1))
    models[MODEL_NAME1] = answer1

    

except Exception as e:
    print(f"Openrouter failed: {e}")

judge_prompt = f"""
You are an expert evaluator. Compare these two AI answers.

QUESTION: {question}

{MODEL_NAME}: {answer}

{MODEL_NAME1}: {answer1}

Which is better? Reply with ONLY the name of the winner: '{MODEL_NAME}', '{MODEL_NAME1}', or 'Tie'.
"""

print("Judge is deciding....")

judge_response = openrouter.chat.completions.create(model="nex-agi/deepseek-v3.1-nex-n1:free",
messages=[{"role":"user","content":judge_prompt}])

winner = judge_response.choices[0].message.content
print(f"And the winner is......{winner} for answer: {models[winner]}")