import os
import sys

from openai import OpenAI
from pydantic import BaseModel


class ResponseFormat(BaseModel):
    urls: list[str]


client = OpenAI(base_url="http://localhost:11434/v1", api_key="dummy")

with open("sample.txt") as f:
    text = f.read()

with open("system_prompt.txt") as f:
    system_prompt = f.read()

resp = client.responses.parse(
    model=os.environ["MODEL_NAME"],
    input=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": "Next, I will provide the markdown text of an index for documents published on the web. Please extract the URLs from it.",
        },
        {"role": "user", "content": text},
    ],
    text_format=ResponseFormat,
    # reasoning={"effort": "high"},
    # verbosity="medium",
)

with open(f"{sys.argv[0]}.json", "w") as f:
    f.write(resp.model_dump_json(indent=2, ensure_ascii=False))
