from ..Config.config import API
from rich.console import Console
from openai import OpenAI
import AI.SystemInstruction.prompt as prompt 
from ..tool.tools import tools
import json
from rich.console import Console
from ..Agent.agent import Agent

console = Console()
class CLIENT_Error(Exception):
    pass

class API_Error(CLIENT_Error):
    pass


class Client:

    def __init__(self , api : API , gen_ai : OpenAI | None = None , message : list | None = None):
        self._api = api
        self._gen_ai = gen_ai
        self.message = message

    def create_client(self):
            if self._gen_ai is None:
               
              if self._api.api_key:
                self._gen_ai = OpenAI(
                    api_key= self._api.api_key,
                    base_url=self._api.base_url
                )
              else:
                  raise API_Error(f"Api_key  not found for this cleint")

    def request(self , query : str):

            agent = Agent()
            self.message = [
                {
                "role" : "system",
                "content" : prompt.SystemInstruction().instruction()
                }
            ]
            if self._gen_ai is None:
              raise CLIENT_Error(f"for this request client is not created or found")

            self.message.append({
               "role" : "user",
               "content" : query
            })

            while(True):
            

              response = self._gen_ai.chat.completions.create(
               model= self._api.model,
               tools = tools,
               tool_choice="auto",                       
              messages=self.message,
            )

              response_message = response.choices[0].message
              tools_calls = response_message.tool_calls
              
              if not tools_calls:
                 console.print(response_message.content)
                 return self.message
        
              self.message.append({
                "role" : "assistant" ,
                "content" : str(response.choices[0].message),
              })

              self.message = agent.tool_request(tools_calls , self.message)
         

    

                

    