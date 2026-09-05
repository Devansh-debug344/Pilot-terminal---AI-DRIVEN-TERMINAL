import os
from dotenv import load_dotenv
from dataclasses import dataclass
load_dotenv()


@dataclass
class API:

  api_key : str |  None
  model : str | None
  base_url : str | None 

  @classmethod
  def set_api(cls) -> "API":
    api_key = os.getenv("API_KEY")
    model = os.getenv("model")
    base_url = os.getenv("base_url")
    
    if not api_key:
        raise ValueError("API_KEY not set in .env")
    if not model:
        raise ValueError("model not set in .env")
    if not base_url:
        raise ValueError("base_url not set in .env")
    
    return cls(api_key=api_key, model=model, base_url=base_url)
