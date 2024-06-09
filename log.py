from rich import print
import datetime



def warn(msg):
    ts = datetime.datetime.now()
    print(f"[yellow][ WARN ][/yellow] \\[{ts}]   {msg}")

def info(msg):
    ts = datetime.datetime.now()
    print(f"[cyan][ INFO ][/cyan] \\[{ts}]   {msg}")

def ok(msg):
    ts = datetime.datetime.now()
    print(f"[green][  OK  ][/green] \\[{ts}]   {msg}")

def error(msg):
    ts = datetime.datetime.now()
    print(f"[red][FAILED][/red] \\[{ts}]   {msg}")