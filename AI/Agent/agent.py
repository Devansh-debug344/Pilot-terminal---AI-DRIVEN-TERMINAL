from ..tool.tools import tools , read_from_file , write_in_file , shell_commands , web_search , list_directory
import json
from dataclasses import dataclass
import AI.SystemInstruction.prompt as prompt
from ..LLM.client import Client
class Agent:

    def __init__(self , client : Client , message : list | None = None):

        self._message = message
        self._client = client

    def request(self , query : str):  
                if self._message is None: 
                  self._message = [
                    {
                    "role" : "system",
                    "content" : prompt.SystemInstruction().instruction()
                    }
                   ]

    
                self._message.append({
                   "role" : "user",
                   "content" : query
                })
                
                if self._client is None:
                     return f"client is none bro"
                
                while(True):
                  
                  response_message = self._client.send(self._message)
                  tools_calls = response_message.tool_calls
                  
                  if not tools_calls:
                     return response_message.content
                  
                  self._message.append({
                    "role" : "assistant" ,
                    "content" : str(response_message),
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
                elif function_name == "list_directory":
                    res = list_directory(path= function_args.get("path"))

                self._message.append({
                  "tool_call_id": tool_call.id,
                  "role": "tool",
                  "name": function_name,
                  "content": json.dumps(res),

                })