# JotNote

A Unix Command-Line Tool to jot notes.

## Table of Contents

- [Installation](#installation)
- [Commands](#commands)
  - [Add](#add)
  - [Show](#show)
  - [Edit](#edit)
  - [Delete](#delete)

## Installation

```shell
# Update setuptools
$ python3 -m pip install --upgrade setuptools

#Clone repository
$ git clone https://github.com/JonathanGzzBen/JotNote.git

# Install package
$ cd JotNote
$ sudo python3 setup.py install

# Write your notes
$ jotnote
[jotnote show]
No notes found.
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

### Edit

Opens note with corresponding ID in your default text editor.

`$ jotnote edit 1`

### Delete

Delete note with corresponding ID.

```shell
$ jotnote delete 1
Note 1 deleted
```
