#!/usr/bin/env python3

import click
import json
from tabulate import tabulate
from jotnote.note import Note
from jotnote.data import notedata
import jotnote.configuration as configuration

def parse_note(input):
    first_period_index = input.find(".")
    if first_period_index == -1:
        title = ""
        content = input
    else:
        title = input[0:first_period_index:]
        content = input[first_period_index + 1::]
    return (title.strip(), content.strip())

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx=None):
    if ctx.invoked_subcommand is None:
        click.echo("[jotnote show]")
        show()

@cli.command()
def show():
    notes_to_display = []
    config = configuration.get_configuration()
    limit = config["limit"]
    notes = notedata.get_notes(config["orderby"], limit)
    for note in notes:
        id, title = note 
        notes_to_display.append((id, title.replace("\n", " ")))
    click.echo(tabulate(notes_to_display, headers=["Title"], tablefmt="pretty"))

@cli.command()
@click.argument('content', nargs=-1)
def add(content):
    if content:
        content = " ".join(content)
        title, content = parse_note(content)
        notedata.create_note(title, content)
    else:
        add_with_editor()

def add_with_editor():
    content = click.edit()
    content = "".join(content)
    title, content = parse_note(content)
    notedata.create_note(title, content)

@cli.command()
@click.argument('id')
def edit(id):
    id, title, content = notedata.get_note(id)
    if title == "":
        editor_initial_content = content
    else:
        editor_initial_content = title + ".\n" + content
    updated_note_input = click.edit(editor_initial_content)
    if updated_note_input is not None:
        updated_title, updated_content = parse_note(updated_note_input)
        notedata.update_note(id, updated_title, updated_content)

@cli.command()
@click.argument('id')
def delete(id):
    notedata.delete_note(id)
    click.echo(f"Note {id} deleted")

@cli.command()
@click.option("--limit", "-l", help="Limit number of notes displayed.")
@click.option("--orderby", "-o", default="modification",
                type=click.Choice(["modification", "creation"], case_sensitive=False))
def configure(limit, orderby):
    config = configuration.get_configuration() 
    if limit:
        config["limit"] = limit
    config["orderby"] = orderby
    configuration.save_configuration(config)

@cli.command()
@click.argument("filename")
def export(filename):
    all_notes = notedata.get_all_notes()
    with open(filename, "w") as export_file:
        json.dump(all_notes, export_file)

@cli.command(name="import")
@click.argument("filename")
def importnotes(filename):
    with open(filename, "r") as import_file:
        imported_notes = json.load(import_file)
    for note in imported_notes:
        notedata.save_note(note)

def main():
    cli()

if __name__ == "__main__":
    main()
