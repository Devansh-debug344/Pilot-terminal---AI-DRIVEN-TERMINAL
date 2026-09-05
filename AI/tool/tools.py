from pathlib import Path
import os , subprocess, json
from googlesearch import search

def read_from_file(filepath : str) -> dict:
    filepath = Path(filepath)
    with open(file=filepath , mode="r" ) as file:
      try:
          return {"status" : "success" , "content" : file.read()}
      except FileNotFoundError as exc:
           return {"status" : "error" ,  "message" : f"File not found . {exc}"}
      except Exception as exc:
           return {"status" : "error" ,  "message" : f"Error in read from file {exc}"}       

def write_in_file(filepath : str , content :str):
    filepath = Path(filepath)
    with open(file=filepath , mode="w") as file:
          try:
              file.write(content)
              return {"status" : "success" , "message" :f"File write sucessfully in filepath {filepath}"}
          except FileNotFoundError as exc:
                return {"status" : "error" ,  "message" : f"File not found {exc}"} 
          except Exception as exc:
              return {"status" : "error" ,  "message" : f"Error in write file {exc}"} 

def shell_commands(command : str):
    try:
        
        result = subprocess.run(command , shell=True , capture_output=True , text=True)

        return {
            "status" : "success",
            "stdout" : result.stdout,
            "stderr" : result.stderr,
            "returncode" : result.returncode
        }
    except Exception as exc:
       return {"status" : "error" ,  "message" : f"Error in executing shell command {exc}"} 

def web_search(query: str):
    """Search the web for information"""
    try:
        res = search(query , num_results=5)

        final_answer = []
        for i , url in enumerate(res):
           final_answer.append((i , url))

        return {
            "status" : "success",
            "output" : final_answer
            }
       
    
    except BaseException as exc:
        return {"status" : "error" ,  "message" : f"Error in web searching {exc}"} 

def list_directory(path: str):
    """List directory structure"""
    try:
        print(f"\n[DEBUG] Input path: {path}")
        if path == ".":
            path = os.getcwd()
        else:
            path = os.path.expanduser(path)
            path = os.path.abspath(path)

        
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}
        
        if not os.path.isdir(path):
            return {"error": f"Not a directory: {path}"}
        
        ignore = {'__pycache__', '.git', '.venv', 'node_modules', '.pytest_cache'}
        path_obj = Path(path)
        
        def get_tree(directory, prefix="", is_last=True):
            lines = []
            try:
                items = sorted(directory.iterdir())
            except PermissionError as e:
                print(f"[DEBUG] Permission error: {e}")
                return lines
            except Exception as e:
                print(f"[DEBUG] Error iterating: {e}")
                return lines
            
            items = [i for i in items if i.name not in ignore]
            dirs = [i for i in items if i.is_dir()]
            files = [i for i in items if i.is_file()]
            all_items = dirs + files
            
            for i, item in enumerate(all_items):
                is_last_item = (i == len(all_items) - 1)
                connector = "└── " if is_last_item else "├── "
                
                if item.is_dir():
                    lines.append(f"{prefix}{connector}📁 {item.name}/")
                    extension = "    " if is_last_item else "│   "
                    lines.extend(get_tree(item, prefix + extension, is_last_item))
                else:
                    lines.append(f"{prefix}{connector}📄 {item.name}")
            
            return lines
        
        tree_lines = [f"📁 {path_obj.name}/"]
        tree_lines.extend(get_tree(path_obj))
        
        return {
            "path": str(path_obj),
            "structure": "\n".join(tree_lines)
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Exception: {str(e)}"}
    
tools = [
        {
          "type" : "function" , 
          "function" : {
              "name" : "read_from_file",
              "description" : "You only run when user explicitly use word read / Read otherwise not . Read the content of a specified file and do analysis if ask, use this to read file and in the end tell user that you read the file succesfully ",
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
                  },
                  {
    "type" : "function" , 
    "function" : {          
        "name": "list_directory",
        "description": "List files and folders in a directory",
        "parameters": { 
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path (e.g., '.', '/home/devansh/fastapi')"
                }
            },
            "required": ["path"]
        }
    }
}
    ]



    