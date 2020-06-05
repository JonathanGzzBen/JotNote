#!/usr/bin/env python3

import argparse
import click
import sqlite3
import os
from jotnote.note import Note

database_filename = "jotnote.db"

def create_database():
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
        print("Error while creating a sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
    

def save_note(title, content):
    try:
        if not os.path.exists(database_filename):
            create_database()
        sqliteConnection = sqlite3.connect(database_filename)
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = f"""
            INSERT INTO Note
            (title, content)
            VALUES
            ('{title}', '{content}')
        """
        cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def print_notes():
    try:
        sqliteConnection = sqlite3.connect(database_filename)
        cursor = sqliteConnection.cursor()

        sqlite_select_query = """ SELECT * FROM Note """
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        for row in records:
            print(f"Title: {row[1]}")
            print(f"Content: {row[2]}")
        cursor.close()
    except sqlite3.Error as error:
        print("Failes to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx=None):
    if ctx.invoked_subcommand is None:
        print_notes()

def add_with_editor():
    content = click.edit()
    content = "".join(content)
    title = content.split(".")[0]
    content = content.split(".")[1]
    save_note(title, content)

@cli.command()
@click.argument('content', nargs=-1)
def add(content):
    if content:
        content = " ".join(content)
        title = content.split(".")[0]
        content = content.split(".")[1]
        save_note(title, content)
    else:
        add_with_editor()

if __name__ == "__main__":
    cli()
