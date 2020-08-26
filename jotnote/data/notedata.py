#!/usr/bin/env python3

import sqlite3
import os
from datetime import datetime

directory_path = os.path.dirname(__file__)
database_path = os.path.join(directory_path, "jotnote.db")
title_max_length_display = 65


def create_database_if_not_exists():
    if os.path.exists(database_path):
        return
    try:
        sqliteConnection = sqlite3.connect(database_path)
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


def create_note(title, content):
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_path)
        cursor = sqliteConnection.cursor()
        sqlite_insert_query = f"""
            INSERT INTO Note
            (title, content, creation_datetime, modification_datetime)
            VALUES
            (?, ?, ?, ?)
        """
        creation_datetime = datetime.now()
        modification_datetime = datetime.now()
        sqlite_query_arguments = (
            title, content, creation_datetime, modification_datetime)
        cursor.execute(sqlite_insert_query, sqlite_query_arguments)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def save_note(note):
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_path)
        cursor = sqliteConnection.cursor()
        sqlite_insert_query = f"""
            INSERT INTO Note
            (title, content, creation_datetime, modification_datetime)
            VALUES
            (?, ?, ?, ?)
        """
        _, title, content, creation_datetime, modification_datetime = note
        modification_datetime = datetime.now()
        sqlite_query_arguments = (
            title, content, creation_datetime, modification_datetime)
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
        sqliteConnection = sqlite3.connect(database_path)
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
        sqliteConnection = sqlite3.connect(database_path)
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
        sqliteConnection = sqlite3.connect(database_path)
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


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def get_notes(orderby="modification_datetime", limit=0):
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_path)
        cursor = sqliteConnection.cursor()

        if orderby == "creation":
            orderby = "creation_datetime"
        else:
            orderby = "modification_datetime"

        sqlite_select_query = f""" 
            SELECT id,
            CASE
            WHEN length(title) = 0 AND length(content) > {title_max_length_display} THEN (substr(content,0,{title_max_length_display}) || '...')
            WHEN length(title) = 0 THEN substr(content,0,{title_max_length_display})
            WHEN length(title) >= {title_max_length_display} THEN (substr(title,0,{title_max_length_display}) || '...')
            ELSE title
            END AS 'title'
            FROM Note
            ORDER BY {orderby} DESC
        """
        if is_integer(limit) and limit not in ("0", 0):
            sqlite_select_query += f"\nLIMIT {limit}"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def get_all_notes():
    try:
        create_database_if_not_exists()
        sqliteConnection = sqlite3.connect(database_path)
        cursor = sqliteConnection.cursor()

        sqlite_select_all_query = f""" 
            SELECT *
            FROM Note
        """
        cursor.execute(sqlite_select_all_query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
