from ..Config.config import API
from rich.console import Console
from openai import OpenAI
from ..tool.tools import tools
from rich.console import Console

console = Console()
class CLIENT_ERROR(Exception):
    pass

class API_ERROR(CLIENT_ERROR):
    pass


class Client:

    def __init__(self , api : API , gen_ai : OpenAI | None = None):
        self._api = api
        self._gen_ai = gen_ai

    def create_client(self):
                if self._gen_ai is None:
                   
                  if self._api.api_key:
                    self._gen_ai = OpenAI(
                        api_key= self._api.api_key,
                        base_url=self._api.base_url
                    )
                  else:
                      raise API_ERROR(f"Api key  not found for this cleint")

    def send(self , message : list):
        self.create_client()
        response = self._gen_ai.chat.completions.create(
                           model= self._api.model,
                           tools = tools,
                           tool_choice="auto",                       
                          messages=message,
                        )
        return response.choices[0].message
    




         

    

                

    