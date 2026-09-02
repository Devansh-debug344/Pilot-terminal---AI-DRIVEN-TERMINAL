from ..tool.tools import tools , read_from_file , write_in_file , shell_commands , web_search
import json
from dataclasses import dataclass


class Agent:

    @staticmethod
    def tool_request(tools_calls , message : list):
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


                return message.append({
                  "tool_call_id": tool_call.id,
                  "role": "tool",
                  "name": function_name,
                  "content": json.dumps(res),

                })