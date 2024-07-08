import re
from typing import List, Optional


class Assistant:
    def __init__(self,
                 prompt_code_classification: str) -> None:
        self.prompt_code_classification = prompt_code_classification

    def _send(self, content: str) -> str:
        raise NotImplementedError()

    def classify_code(self, attribute: str, system: Optional[str]=None) -> bool:
        res = self._send(self.prompt_code_classification.format(attribute=attribute), system)
        print(res)
        return "PII" in res