
from typing import List, Optional
from Assistant import Assistant
from openai import OpenAI
from prompts import RECORD_CLASSIFICATION


class OpenAssistant(Assistant):
    def __init__(self, 
                 model: str, 
                 base_url: str="http://localhost:11434/v1", 
                 api_key: str="ollama",
                 prompt_code_classification: str=RECORD_CLASSIFICATION) -> None:
        super().__init__(prompt_code_classification)
        self.model: str = model
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def _send(self, content: str, system: Optional[str]=None):
        return self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": content}
            ] if not system else [
                {"role": "system", "content": system},
                {"role": "user", "content": content}
            ],
            temperature=0.0,
            model=self.model,
            max_tokens=2048
        ).choices[0].message.content
