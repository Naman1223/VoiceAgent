from typing import Any
import json
import subprocess
from dataclasses import dataclass
from typing import Callable
import chromadb

@dataclass
class Tools:
    name: str
    description: str
    input_schema: dict
    func: Callable

    @property
    def tool_schema(self) -> dict[str,Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }