# JotNote

A Unix Command-Line Tool to jot notes.

## Commands

### Add

#### Syntax

`jotnote add [options] [title]`

This will create a note with given title. You don't need to enclose it with quotes.

#### Examples

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

```text
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

`$ jotnote show`

This is the default command, you can also use:

`$ jotnote`
