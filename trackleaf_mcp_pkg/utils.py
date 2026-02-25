import os
import json
from typing import Any
from dotenv import load_dotenv

load_dotenv()

def env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v


def to_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)
