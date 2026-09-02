from .config import API
from rich.console import Console
from openai import OpenAI
import AI.cli as cl
from .tools import tools , read_from_file , write_in_file , shell_commands , web_search
import json
from rich.console import Console

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
        
            self.message = [
                {
                "role" : "system",
                "content" : cl.SystemInstruction().instruction()
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

              self.tool_request(tools_calls)
         

    def tool_request(self , tools_calls):
            for tool_call in tools_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "read_from_file":
                    res = read_from_file(filepath=function_args.get("filepath"))
                elif function_name == "write_in_file":
                    res = write_in_file(filepath=function_args.get("filepath") , content=function_args.get("content"))
                elif function_name == "shell_commands":
                    res = shell_commands(command=function_args.get("command"))

                elif function_name == "web_search":
                    res = web_search(query=function_args.get("query"))


                self.message.append({
                  "tool_call_id": tool_call.id,
                  "role": "tool",
                  "name": function_name,
                  "content": json.dumps(res),

                })

                

    