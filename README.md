# JotNote

A Unix Command-Line Tool to jot notes.

## Table of Contents

- [Installation](#installation)
  - [Uninstall](#uninstall)
- [Commands](#commands)
  - [Add](#add)
  - [Show](#show)
  - [Edit](#edit)
  - [Delete](#delete)
  - [Configure](#configure)

## Installation

### From release

Download [latest release](https://github.com/JonathanGzzBen/JotNote/releases/latest), head to downloads directory and install using [pip](https://pypi.org/project/pip/).

```shell
pip install JotNote-1.0.1.tar.gz
```

### From repository
```shell
# Update setuptools
$ pip install --upgrade setuptools

# Clone repository
$ git clone https://github.com/JonathanGzzBen/JotNote.git

# Install package
$ (cd JotNote && pip install .)

# Write your notes
$ jotnote
[jotnote show]
No notes found.
```

### Uninstall

```shell
# Uninstall package
$ pip uninstall jotnote

# Remove data and configurations
$ rm ~/.jotnote -r
```

## Commands

### Add

This will create a note with given title. You don't need to enclose it with quotes.

`$ jotnote add This is the title`

```json
{
  "id": 1,
  "title": "This is the title"
}
```

You can immediately define title and content, separating it with a `.`

`$ jotnote add This is the title. And this is the content`

```json
{
  "id": 1,
  "title": "This is the title.",
  "content": "And this is the content"
}
```

You can also execute it without any parameter to write your note in your default text editor.

`$ jotnote add`

If you save and quit in your text editor after writing this:

```shell
This is the title.
And this the content
```

You will get this:

```json
{
  "id": 1,
  "title": "This is the title.",
  "content": "And this is the content"
}
```

### Show

Displays your notes, you can change the maximum number of notes displayed and the sort method using the `configure` command.

```shell
$ jotnote show

+---+------------------------------------+
|   |               Title                |
+---+------------------------------------+
| 2 |            Second note             |
| 1 | This is the title of my first note |
+---+------------------------------------+
```

This is the default command, you can also use:

```shell
$ jotnote
[jotnote show]

+---+------------------------------------+
|   |               Title                |
+---+------------------------------------+
| 2 |            Second note             |
| 1 | This is the title of my first note |
+---+------------------------------------+
```

You can directly print the contents of a note by passing the Id to the `show` command.

```shell
$ jotnote show 1

This is the title of my first note.

And this is the content.
```

### Edit

Opens note with corresponding ID in your default text editor.

`$ jotnote edit 1`

### Delete

Delete note with corresponding ID.

```shell
$ jotnote delete 1

Note 1 deleted
```

### Configure

Check or modify your configurations.

```shell
$ jotnote configure --help
Usage: jotnote configure [OPTIONS]

Options:
  -l, --limit INTEGER             Limit number of notes displayed.
  -o, --orderby [modification|creation]
  --help                          Show this message and exit.
```

If you pass no options, your current configurations will be printed.

```shell
$ jotnote configure

Configuration    Value
---------------  --------
limit            5
orderby          creation
```
