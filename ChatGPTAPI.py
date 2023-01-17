import openai
openai.api_key = "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"

response = openai.Completion.create(
    engine="text-davinci-002",
    prompt='What is ChatGPT ?',
    max_tokens=1024
)
print(response["choices"][0]["text"])
