from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-sol",
    input="Explain Django in one simple sentence."
)

print(response.output_text)