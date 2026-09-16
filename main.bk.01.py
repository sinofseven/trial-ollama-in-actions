import json
import os
import sys
from collections.abc import Iterable

from openai import OpenAI
from pydantic import BaseModel


class ResponseFormat(BaseModel):
    urls: list[str]


def chunks(text: str, lines_per_chunk: int = 40) -> Iterable[str]:
    lines = text.splitlines()

    for i in range(0, len(lines), lines_per_chunk):
        yield "\n".join(lines[i : i + lines_per_chunk])


def main():
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="dummy")

    with open("sample.txt") as f:
        text = f.read()

    with open("system_prompt.txt") as f:
        system_prompt = f.read()

    all_urls: list[str] = []

    for i, chunk in enumerate(chunks(text)):
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
                {"role": "user", "content": chunk},
            ],
            text_format=ResponseFormat,
            # reasoning={"effort": "high"},
            # verbosity="medium",
        )

        with open(f"{sys.argv[0]}.0.raw.{i}.json", "w") as f:
            f.write(resp.model_dump_json(indent=2, ensure_ascii=False))

        all_urls.extend(resp.output_parsed.urls)

    with open(f"{sys.argv[0]}.1.result.json", "w") as f:
        json.dump(all_urls, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
