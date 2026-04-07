

import requests

response = requests.post(
    url="https://api.featherless.ai/v1/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer rc_f4d5e19e036bd1dd61015b9b614dfd8f0b1967498332a23c4c09b6d932e0ccbc"
    },
    json={
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! How are you?"}
        ]
    }
)
print(response.json()["choices"][0]["message"]["content"])