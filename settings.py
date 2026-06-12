import os

import urllib3
from dotenv import load_dotenv

load_dotenv()


def is_truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


DEBUG = is_truthy(os.environ.get("DEBUG", "false"))
VERIFY_SSL = is_truthy(os.environ.get("VERIFY_SSL", "true"))
REQUEST_TIMEOUT_SECONDS = int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "10"))
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)