# NoteServeCLI
A command-line tool to access your NoteServe notes

## Installation
```
python -m pip install -r requirements.txt
```

## Usage

### List notes
List all notes in server
```
nscli.py -l
nscli.py --list
```

### Create note
Create a new note
```
nscli.py -c NAMEOFNOTE
nscli.py --create NAMEOFNOTE
```

### Edit note
Edit a existing note
```
nscli.py -e NAMEOFNOTE
nscli.py --edit NAMEOFNOTE
```

### Peak note
Prints the note to stdout
```
nscli.py -p NAMEOFNOTE
nscli.py --peak NAMEOFNOTE
```

### Delete note
Deletes a note
```
nscli.py -d NAMEOFNOTE
nscli.py --delete NAMEOFNOTE
```