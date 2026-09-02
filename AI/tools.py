from pathlib import Path
import subprocess, json
from googlesearch import search
def read_from_file(filepath : str) -> dict:
    filepath = Path(filepath)
    with open(file=filepath , mode="r" ) as file:
      try:
          
          return {"status" : "success" , "content" : file.read()}
      except FileNotFoundError as exc:
           raise (f'file not found in system . Error shows {exc}')
      except Exception as exc:
           raise (f"Error in read from file . {exc}")       

def write_in_file(filepath : str , content :str):
    file_path = Path(filepath)
    with open(file=filepath , mode="w") as file:
          try:
              file.write(content)
              return {"status" : "success" , "message" :f"File read sucessfully in filepath {filepath}"}
          except FileNotFoundError as exc:
               raise (f'file not found in system . Error shows {exc}')
          except Exception as exc:
               raise (f"Error in read from file . {exc}")

def shell_commands(command : str):
    try:
        subprocess.run(command , shell=True)
    except Exception as exc:
        raise (f"Error in excecuting shell_commands. {exc}")       

def web_search(query: str):
    """Search the web for information"""
    
    

    try:
        res = search(query , num_results=5)

        final_answer = []
        print("i am stan lee")
        for i , url in enumerate(res):
           final_answer.append((i , url))

        return final_answer   
    
    except BaseException as e:
        raise(f"error: Search failed: {str(e)} and query: {query}")

tools = [
        {
          "type" : "function" , 
          "function" : {
              "name" : "read_from_file",
              "description" : "You only run when user explicilty use word read / Read otherwise not . Read the content of a specified file and do analysis if ask, use this to read file and in the end tell user that you read the file succesfully ",
               "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path of the file to read, e.g., '/home/devansh/data.txt' and when done say user that you write the file succesfully",
                    }
                },
                "required": ["filepath"],
            }
          }
         },
         {
         "type" : "function" , 
                   "function" : {
                       "name" : "write_in_file",
                       "description" : "Write content to a file",
                        "parameters": {
                         "type": "object",
                         "properties": {
                            "filepath": {"type": "string"},
                            "content": {"type": "string"}
                         },
                         "required": ["filepath" , "content"],
                     }
                   }
         },
         {
             "type" : "function" , 
              "function" : {
                  "name" : "shell_commands",
                  "description" : "RUN SHELL COMMANDS like tests, linting, etc. NOT for reading files. Use this but not to read files and write files.And also tell you execute the command succesfully to user ",
              "parameters" : {
                  "type" : "object",
                  "properties" : {
                      "command" : {
                        "type" :  "string",
                        "description": "Shell command to execute"
                        }
                  },
                "required" : ["command"] ,
                  
              }
              }
         },
         {
            "type" : "function" , 
                "function" : {
                    "name" : "web_search",
                    "description" : "Search the internet for information, documentation, tutorials, current info",
                       "parameters" : {
                           "type" : "object",
                           "properties" : {
                               "query" : {
                                 "type" :  "string",
                                 "description": "What to search for"
                                 }
                           },
                         "required" : ["query"],      
                       }
                       }
                  }
    ]



    