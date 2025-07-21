import typer

from modulus.cli import commands

app = typer.Typer()

@app.command()
def init(directory: str = ".") -> None:
    commands.init(directory)

@app.command()
def verify() -> None:
    commands.verify()

@app.command()
def plan() -> None:
    commands.plan()

@app.command()
def apply() -> None:
    commands.apply()


@app.command()
def run() -> None:
    commands.run()


@app.command()
def show() -> None:
    commands.show()

@app.command()
def destroy() -> None:
    commands.destroy()
