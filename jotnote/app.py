#!/usr/bin/env python3

import argparse
from jotnote.note import Note

def run():
    parser = argparse.ArgumentParser(description='Jot a note')
    parser.add_argument('-c', '--content', type=str, help='content of the note', required=True)
    parser.add_argument('-t', '--title', type=str, help='title of the note', required=False)
    args = parser.parse_args()
    note = Note(args.content, args.title)
    print(note.content)
    return

if __name__ == "__main__":
    run()
