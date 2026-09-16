from openai import OpenAI
from pydantic import BaseModel


class ResponseFormat(BaseModel):
    urls: list[str]


client = OpenAI(base_url="http://localhost:11434/v1", api_key="dummy")

with open("sample.txt") as f:
    text = f.read()

resp = client.responses.parse(
    model="gemma4:e2b",
    input=[
        {
            "role": "system",
            "content": "Please extract URLs from the markdown text provided by the user.",
        },
        {"role": "user", "content": text},
    ],
    text_format=ResponseFormat,
)
