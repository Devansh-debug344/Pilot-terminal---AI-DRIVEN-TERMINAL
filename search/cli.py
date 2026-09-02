import typer , os 
from pathlib import Path
from rich.console import Console
app = typer.Typer()

console = Console()

@app.command()
def search(path : str) -> None:

    # path = Path(path)

    console.print(os.listdir(path))

@app.command()
def parser(ls : str) -> None:
    # dic = {"startswith" : "^" , "endswith" : "$" , "and" : ".*"}

    c=0
    res = []
    for i in ls.split():
        if i == "startswith":
            res.append("^")
        elif i == "and":
            res.append(".*")
        elif i == "endswith":
            res.append("$")
        else:
            break
        
    console.print(res)

if __name__ == "__main__":
      app()