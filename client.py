from openai import OpenAI
 
# pip install openai 
# Replace "<Your Key Here>" with your actual OpenAI API key from https://platform.openai.com/account/api-keys
# Example: api_key="sk-proj-abc123..."
client = OpenAI(
  api_key="<Your Key Here>",  # Replace this with your actual API key
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)