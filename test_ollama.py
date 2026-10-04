import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Explain Django in one simple sentence."
        }
    ]
)

print(response["message"]["content"])