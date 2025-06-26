import typer

from modulus.cli import commands

app = typer.Typer()

@app.command()
def init(directory: str = "."):
    commands.init(directory)

@app.command()
def verify():
    commands.verify()

@app.command()
def plan():
    commands.plan()

@app.command()
def apply():
    commands.apply()

@app.command()
def show():
    commands.show()

@app.command()
def destroy():
    commands.destroy()
