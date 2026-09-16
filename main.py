import os
import sys

from openai import OpenAI
from pydantic import BaseModel


class ResponseFormat(BaseModel):
    urls: list[str]


client = OpenAI(base_url="http://localhost:11434/v1", api_key="dummy")

with open("sample.txt") as f:
    text = f.read()

resp = client.responses.parse(
    model=os.environ["MODEL_NAME"],
    input=[
        {
            "role": "system",
            "content": "Please extract all URLs from the markdown text provided by the user.",
        },
        {"role": "user", "content": text},
    ],
    text_format=ResponseFormat,
    # reasoning={"effort": "high"},
    # verbosity="medium",
)

with open(f"{sys.argv[0]}.json", "w") as f:
    f.write(resp.model_dump_json(indent=2, ensure_ascii=False))
