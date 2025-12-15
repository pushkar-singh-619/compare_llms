import os
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv(override=True)

reader = PdfReader("program/pdf/ebook.pdf")

print(f"Number of pages: {len(reader.pages)}")

# page = reader.pages[15]
# text = page.extract_text()

# print(text)


def extract_text_from_range(pdf_path, start_page, end_page):
    reader = PdfReader(pdf_path)
    full_text = ""

    for i in range(start_page, end_page):
        page = reader.pages[i]
        full_text += page.extract_text()

    return full_text

# --- Usage ---
# Extract text from Page 3 to Page 5
extracted_content = extract_text_from_range("program/pdf/ebook.pdf", 15, 22)
# print(extracted_content)

prompt = f"Summarize this chapter one of Rich Dad Poor Dad: {extracted_content}"

base_url = "https://openrouter.ai/api/v1"
api_key = os.getenv("OPENROUTER_API_KEY")

deepseek = OpenAI(base_url=base_url, api_key=api_key)


model_name = "nex-agi/deepseek-v3.1-nex-n1:free"
print(f"Connecting to openrouter model: {model_name}\n\n\n\n\n")

messages = [{"role": "user", "content": prompt}]
response = deepseek.chat.completions.create(model=model_name, messages=messages)

summary = response.choices[0].message.content
print(f"\n\n\n\nSummary of Chapter 1 of Rich Dad Poor Dad: {summary}")

