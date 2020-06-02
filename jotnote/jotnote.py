#!/usr/bin/env python3

import argparse

def run():
    print("Hey")
    parser = argparse.ArgumentParser(description='Jot a note')
    parser.add_argument('content', type=str, help='content of the note')
    return

if __name__ == "__main__":
    run()