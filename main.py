import os

from openai import OpenAI
from pydantic import BaseModel


class ResponseFormat(BaseModel):
    nums: list[int]


client = OpenAI(base_url="http://localhost:11434/v1", api_key="dummy")

resp = client.responses.parse(
    model=os.environ["MODEL_NAME"],
    input=[
        {
            "role": "user",
            "content": "Please calculate the first 30 numbers of the Fibonacci sequence and output them as an array.",
        }
    ],
    text_format=ResponseFormat,
)

## Debugのために全部出力する
print(resp.model_dump_json(indent=2, ensure_ascii=False))
