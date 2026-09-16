import os
import warnings

from openai import OpenAI
from pydantic import BaseModel

# 構造化アウトプットで警告が出るため
warnings.filterwarnings("ignore", module="pydantic")


class ResponseFormat(BaseModel):
    nums: list[int]


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="dummy",  # ollamaでは必要ないけど必須なので
)

resp = client.responses.parse(
    model=os.environ["MODEL_NAME"],
    input="Please calculate the first 20 numbers of the Fibonacci sequence and output them as an array.",
    text_format=ResponseFormat,
)

## Debugのために全部出力する
print(resp.model_dump_json(indent=2, ensure_ascii=False))
