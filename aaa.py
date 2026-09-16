import os

from openai import OpenAI
from pydantic import BaseModel


class ResponseFormat(BaseModel):
    nums: list[int]


client = OpenAI(
    base_url="http://localhost:11434",
    api_key="dummy",  # ollamaでは必要ないけど必須なので
)

resp = client.responses.parse(
    model=os.environ["MODEL_NAME"],
    text_format=ResponseFormat,
    input="Please calculate the first 30 numbers of the Fibonacci sequence and output them as an array.",
)

print(resp.model_dump_json(indent=2, ensure_ascii=False))
