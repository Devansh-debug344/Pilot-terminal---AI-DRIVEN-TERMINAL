import os
from dotenv import load_dotenv
from dataclasses import dataclass
load_dotenv()


@dataclass
class API:

    api_key : str
    model : str | None
    base_url : str 
    @classmethod
    def set_api(cls) -> "API":
      
      return cls(
        model = os.getenv("model"),
        api_key = os.getenv("API_KEY"),
        base_url = os.getenv("base_url")
      )
