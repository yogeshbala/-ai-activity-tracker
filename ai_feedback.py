import openai
from config import get_openai_key

openai.api_key = get_openai_key()

def generate_suggestions(task, reason):
    prompt = f"I skipped '{task}' because '{reason}'. Suggest a motivational tip or improvement."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Couldn't generate suggestion."
