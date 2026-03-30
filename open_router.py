import requests
import json

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
        # Optional. Site URL for rankings on openrouter.ai.
        "HTTP-Referer": "Martify.store",
        # Optional. Site title for rankings on openrouter.ai.
        "X-OpenRouter-Title": "Martify",
    },
    data=json.dumps({
        "model": "qwen/qwen3-coder:free",
        "messages": [
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
        ]
    })
)
