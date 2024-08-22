from groq import Groq
import time
from config import GROK_API_KEY
client = Groq(
# This is the default and can be omitted
api_key=GROK_API_KEY,
)

messages = {
    "role": "system",
    "content": "You need to perform the task given by the user"
    }

def LLM(prompt):
    time.sleep(5)
    global messages
    # Append user message to messages list
    messages.append({"role": "system", "content": prompt})

    # Create client and get response
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192"
        )
        # Extract assistant message from response
        ms = chat_completion.choices[0].message.content

        # Append assistant message to messages list
        messages.append({"role": "assistant", "content": ms})

        return ms
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
