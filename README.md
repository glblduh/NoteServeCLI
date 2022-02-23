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
main.py -l
main.py --list
```

### Create note
Create a new note
```
main.py -c NAMEOFNOTE
main.py --create NAMEOFNOTE
```

### Edit note
Edit a existing note
```
main.py -e NAMEOFNOTE
main.py --edit NAMEOFNOTE
```

### Peak note
Prints the note to stdout
```
main.py -p NAMEOFNOTE
main.py --peak NAMEOFNOTE
```

### Delete note
Deletes a note
```
main.py -d NAMEOFNOTE
main.py --delete NAMEOFNOTE
```