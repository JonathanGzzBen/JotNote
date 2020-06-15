#!/usr/bin/env python3

import sqlite3
import os
from datetime import datetime

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
                content TEXT NOT NULL,
                creation_datetime TEXT NOT NULL,
                modification_datetime TEXT NOT NULL);
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
            (title, content, creation_datetime, modification_datetime)
            VALUES
            (?, ?, ?, ?)
        """
        creation_datetime = datetime.now()
        modification_datetime = datetime.now()
        sqlite_query_arguments = (title, content, creation_datetime, modification_datetime)
        cursor.execute(sqlite_insert_query, sqlite_query_arguments)
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
                content=?,
                modification_datetime=?
            WHERE
                id=?;
        """
        modification_date = datetime.now()
        sqlite_query_arguments = (title, content, modification_date, id)
        cursor.execute(sqlite_update_query, sqlite_query_arguments)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to update note", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def delete_note(id):
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_filename)
        cursor = sqliteConnection.cursor()

        sqlite_delete_query = f"""
            DELETE FROM Note
            WHERE id=?
        """
        cursor.execute(sqlite_delete_query, (id))
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete node", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def get_note(id):
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_filename)
        cursor = sqliteConnection.cursor()
        sqlite_get_note_query = f"""
            SELECT id, title, content
            FROM Note
            WHERE id=?
        """
        cursor.execute(sqlite_get_note_query, (id))
        note_found = cursor.fetchone()
        cursor.close()
        return note_found
    except sqlite3.Error as error:
        print("Could not get note from database", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def get_notes(order_by="modification_datetime"):
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_filename)
        cursor = sqliteConnection.cursor()

        sqlite_select_query = f""" 
            SELECT id,
            CASE
            WHEN length(title) = 0 AND length(content) > {title_max_length_display} THEN (substr(content,0,{title_max_length_display}) || '...')
            WHEN length(title) = 0 THEN substr(content,0,{title_max_length_display})
            WHEN length(title) >= {title_max_length_display} THEN (substr(title,0,{title_max_length_display}) || '...')
            ELSE title
            END AS 'title'
            FROM Note
            ORDER BY modification_datetime DESC;
        """
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
