#!/usr/bin/env python3

import argparse
import click
from jotnote.note import Note

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx=None):
    if ctx.invoked_subcommand is None:
        click.echo("List notes")

def addWithEditor():
    content = click.edit()
    content = "".join(content)
    title = content.split(".")[0]
    content = content.split(".")[1]
    click.echo("Title: " + title)
    click.echo("Content: " + content)

@cli.command()
@click.argument('content', nargs=-1)
def add(content):
    if content:
        content = " ".join(content)
        title = content.split(".")[0]
        content = content.split(".")[1]
        click.echo("Title: " + title)
        click.echo("Content: " + content)
    else:
        addWithEditor()

if __name__ == "__main__":
    cli()
