#!/usr/bin/env python3
import requests 
import json
import argparse
import getpass
import sys
import os
import urllib3
from prettytable import PrettyTable
import subprocess
import time
from rich.console import Console
from rich.markdown import Markdown

# Suppress InsecureRequestWarning caused by disabled verification of certificates in Requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Declaring of arguments to argparse
parser = argparse.ArgumentParser(description="A command-line utility for your NoteServe server")
group = parser.add_mutually_exclusive_group()
group.add_argument("-l", "--list", help="List all notes", action="store_true")
group.add_argument("-c", "--create", type=str, help="Create a note")
group.add_argument("-e", "--edit", type=str, help="Edit a note")
group.add_argument("-d", "--delete", type=str, help="Delete a note")
group.add_argument("-p", "--peak", type=str, help="Prints raw note")

if __name__ == "__main__":
    # Path of config file
    confpath = os.path.expanduser("~/.noteservecli.json")

    # Shows usage if no arguments are provided
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    else:
        args = parser.parse_args()

    # Check if config file exist else create it    
    if not os.path.exists(confpath):
        f = open(confpath, "w")
        f.write(json.dumps({
            "apikey": "",
            "serverurl": "http://example.com",
            "noverifytls": False,
            "serverport": 8787,
            "editorpath": "",
            "editorargs": ""
        }, indent=4))
        f.close()
        print("Config not found. Edit file on \"" + confpath + "\" to be able to use the program")
        sys.exit(1)

    # Parse config file
    f = open(confpath, "r")
    conf = json.loads(f.read())
    f.close()
    key = conf["apikey"]
    server = conf["serverurl"] + "/api"
    port = conf["serverport"]
    disableVerify = not conf["noverifytls"]
    editorPath = conf["editorpath"]
    editorArgs = conf["editorargs"]

    # Key checking
    res = requests.get(server + "/allnotes", headers={
        "Authorization": "Bearer " + key
    }, verify=disableVerify).json()
    if "error" in res:
        print("[ERROR] " + res["error"])
        sys.exit(1)


    # Activated with --list or -l argument
    if args.list:
        res = requests.get(server + "/allnotes", headers={
            "Authorization": "Bearer " + key
        }, verify=disableVerify).json()
        listable = PrettyTable(["Note Name", "Time Added", "First 15 chars"])
        for note in res:
            listable.add_row([note, time.strftime("%m-%d-%Y %H:%M", time.localtime(res[note]["timeadded"]/1000)), res[note]["note"][:15]])
        print(listable)
        sys.exit(0)

    # Activated with --create or -c argument
    if args.create is not None:
        fn = "." + args.create + ".noteserve.tmp"
        f = open(fn, "w")
        f.close()
        print("Waiting for editor to be closed...")
        if editorArgs != "":
            subprocess.Popen([editorPath, editorArgs, fn]).wait()
        else:
            subprocess.Popen([editorPath, fn]).wait()
        print("Editor closed. Saving to server as \"" + args.create + "\"")
        f = open(fn, "r")
        res = requests.post(server + "/addnote", headers={
            "Authorization": "Bearer " + key
        }, verify=disableVerify, json={
            "name": args.create,
            "note": f.read()
        }).json()
        f.close()
        timesaved = time.strftime("%m-%d-%Y %H:%M", time.localtime(res["timeadded"]/1000))
        os.remove(fn)
        print("Note saved as \"" + args.create + "\" on " + timesaved)
        sys.exit(0)

    # Activated with --delete or -d argument
    if args.delete is not None:
        res = requests.delete(server + "/removenote/" + args.delete, headers={
            "Authorization": "Bearer " + key
        }, verify=disableVerify).json()
        if not "error" in res:
            print("Note successfully deleted on " + time.strftime("%m-%d-%Y %H:%M", time.localtime(res["timeremoved"]/1000)))
            sys.exit(0)
        else:
            print("[ERROR] " + res["error"])
            sys.exit(1)

    # Activated with --edit or -e argument
    if args.edit is not None:
        res = requests.get(server + "/allnotes", headers={
            "Authorization": "Bearer " + key
        }, verify=disableVerify).json()
        if not args.edit in res:
            print("[ERROR] Note named \"" + args.edit + "\" is not found on server")
            sys.exit(1)
        fn = "." + args.edit + ".noteserve.tmp"
        f = open(fn, "w")
        f.write(res[args.edit]["note"])
        f.close()
        print("Waiting for editor to be closed...")
        if editorArgs != "":
            subprocess.Popen([editorPath, editorArgs, fn]).wait()
        else:
            subprocess.Popen([editorPath, fn]).wait()
        print("Editor closed. Saving to server as \"" + args.edit + "\"")
        f = open(fn, "r")
        res = requests.post(server + "/addnote", headers={
            "Authorization": "Bearer " + key
        }, verify=disableVerify, json={
            "name": args.edit,
            "note": f.read()
        }).json()
        f.close()
        timesaved = time.strftime("%m-%d-%Y %H:%M", time.localtime(res["timeadded"]/1000))
        os.remove(fn)
        print("Note saved as \"" + args.edit + "\" on " + timesaved)
        sys.exit(0)

    # Activated with --peak or -p argument
    if args.peak is not None:
        res = requests.get(server + "/allnotes", headers={
            "Authorization": "Bearer " + key
        }, verify=disableVerify).json()
        if not args.peak in res:
            print("[ERROR] Note named \"" + args.peak + "\" is not found on server")
            sys.exit(1)
        Console().print(Markdown(res[args.peak]["note"]))
        sys.exit(0)