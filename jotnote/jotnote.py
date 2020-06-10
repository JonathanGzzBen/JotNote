#!/usr/bin/env python3

import click
from tabulate import tabulate
import sqlite3
import os
from jotnote.note import Note

database_filename = "jotnote.db"
title_max_length_display = 35

def create_database_if_not_exists():
    if os.path.exists(database_filename):
        return
    try:
        sqliteConnection = sqlite3.connect(database_filename)
        sqlite_create_table_query = """
            CREATE TABLE IF NOT EXISTS Note (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            );
        """
        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while creating sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def save_note(title, content):
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_filename)
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = f"""
            INSERT INTO Note
            (title, content)
            VALUES
            (?, ?)
        """
        cursor.execute(sqlite_insert_query, (title, content))
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def update_note(id, title, content):
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_filename)
        cursor = sqliteConnection.cursor()

        sqlite_update_query = f"""
            UPDATE Note
            SET
                title=?,
                content=?
            WHERE
                id=?;
        """

        cursor.execute(sqlite_update_query, (title, content, id))
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to update note", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def print_notes():
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_filename)
        cursor = sqliteConnection.cursor()

        sqlite_select_query = f""" 
            SELECT id,
            CASE
            WHEN length(title) >= {title_max_length_display} THEN (substr(title,0,{title_max_length_display}) || '...')
            ELSE title
            END AS 'title'
            FROM Note
        """
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print(tabulate(records, headers=["Title"]))
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def parse_note(input):
    first_period_index = input.find(".")
    if first_period_index == -1:
        title = input[0:title_max_length_display + 1:]
        content = input
    else:
        title = input[0:first_period_index:]
        content = input[first_period_index + 1::]
    return (title.strip(), content.strip())

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx=None):
    if ctx.invoked_subcommand is None:
        print_notes()

def add_with_editor():
    content = click.edit()
    content = "".join(content)
    title, content = parse_note(content)
    save_note(title, content)

@cli.command()
@click.argument('id')
def edit(id):
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_filename)
        cursor = sqliteConnection.cursor()

        sqlite_get_note_query = f"""
            SELECT title, content
            FROM Note
            WHERE id=?;
        """
        cursor.execute(sqlite_get_note_query, (id))
        title, content = cursor.fetchone()
        cursor.close()
        editor_initial_content = title + ".\n" + content
        updated_note_input = click.edit(editor_initial_content)
        if updated_note_input is not None:
            updated_title, updated_content = parse_note(updated_note_input)
            update_note(id, updated_title, updated_content)
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


@cli.command()
@click.argument('content', nargs=-1)
def add(content):
    if content:
        content = " ".join(content)
        title, content = parse_note(content)
        save_note(title, content)
    else:
        add_with_editor()

def main():
    cli()

if __name__ == "__main__":
    main()
