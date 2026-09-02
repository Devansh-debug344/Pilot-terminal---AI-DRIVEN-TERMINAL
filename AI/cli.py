import typer , os 
from pathlib import Path
from rich.console import Console
from .client import Client , CLIENT_Error , API_Error  
from .config import API
import subprocess
from .cliscreen import welcome_screen
# import tkinter as tk
# from tkinter import filedialog



app = typer.Typer()

console = Console()

# welcome_screen()

class SystemInstruction:
    def __init__(self , system_instruction = None):
        self._system_instruction = system_instruction

    def instruction(self):
        self._system_instruction = """You are ait, an AI terminal assistant.

YOU CAN:
1. Debug and fix local code files
2. Search the internet for information
3. Have casual conversations
4. Answer any question
5. Dont do web search if you already know the answer.
TOOLS AVAILABLE:
1. read_from_file(filepath) - Read local files
2. write_in_file(filepath, content) - Save code
3. execute_command(command) - Run shell commands
4. web_search(query) - Search internet for information

WHEN TO USE EACH:

CODE DEBUGGING:
- User: "Fix fun.py" → read_from_file + write_in_file
- User: "Does this work?" → execute_command to test
- User: "What's in storage.py?" → read_from_file

INTERNET SEARCH:
- User: "What's FastAPI?" → web_search("FastAPI")
- User: "How do I use async/await?" → web_search("async await Python")
- User: "Latest Node.js version?" → web_search("Node.js latest version")

CASUAL CHAT (no tools needed):
- User: "Tell me a joke" → Just respond, no tools
- User: "What's the weather?" → web_search if they ask current weather
- User: "How do I learn Python?" → Respond directly OR search for resources
- User: "What are you?" → Just respond

SMART RULES:
1. Detect what type of request it is
2. Use appropriate tool OR just respond
3. Don't use tools unnecessarily
4. For casual questions, you can:
   - Answer from knowledge
   - OR search internet if they ask for current info
5. Combine tools when helpful:
   - Read their code + search documentation = better help

RESPONSE STYLE:
- For code: Technical, precise
- For search: Summarize findings, add context
- For casual: Friendly, conversational
- Always be helpful and clear"""
        return self._system_instruction   

def get_response(query : str):
        try:
         client = Client(API.set_api()) 
         client.create_client()
         res = client.request(query)

         return res

        except CLIENT_Error as ce:
           raise(f'error {ce} in search function')


# def gui():
#     root = tk.Tk()
#     root.title("PILOT TERMINAL")

#     tk.Label(root, text="Filename").pack()
#     filename_entry = tk.Entry(root, width=40)
#     filename_entry.pack()

#     tk.Label(root, text="Threshold").pack()
#     threshold_entry = tk.Entry(root)
#     threshold_entry.insert(0, "0.8")
#     threshold_entry.pack()

#     def run():
#         filename = filename_entry.get()
#         threshold = float(threshold_entry.get())
#         process_file(filename, threshold)

#     tk.Button(root, text="Process", command=run).pack(pady=10)

#     root.mainloop()


@app.command()
def search(query : str) -> None:

    messages = get_response(query)

    # console.print(messages[len(messages) - 1].get('content'))
    # console.print(messages)
    console.print("\n✨ Done!\n")



if __name__ == "__main__":
      app()