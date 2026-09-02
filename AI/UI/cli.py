import typer , os 
from pathlib import Path
from rich.console import Console
from ..LLM.client import Client , CLIENT_Error , API_Error  
from AI.Config.config import API
import subprocess
from .cliscreen import welcome_screen
# import tkinter as tk
# from tkinter import filedialog



app = typer.Typer()

console = Console()

# welcome_screen()


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