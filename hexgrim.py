#!/usr/bin/env python3

import os

import click
import tomlkit

CONFIG_FILE = os.path.expanduser("~/.config/hexgrim/hexgrim.toml")


# TODO: good comments necessary
# TODO: Make exceptions better
# TODO: Cleanup
# TODO: Testing
# TODO: Fix Spacing
# : standardize messages
# TODO Prep for packaging
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        with open(CONFIG_FILE, "r") as f:
            doc = tomlkit.load(f)
        # TODO Get this outputting in neat clean columns for piping to less
        for name, desc in sorted(doc["commands"].items()):
            print(name, ":", desc["description"])


# : standardize messages
# : Add feedback for when a fresh file is made
# NOTE: Possibly change confirmation dialog
@cli.command()
def new():
    config_dir = os.path.expanduser("~/.config/hexgrim/")
    os.makedirs(config_dir, exist_ok=True)

    if os.path.exists(CONFIG_FILE):
        while True:
            print(
                "A grimoire already exists, do you choose to purge it and start anew?"
            )
            print("Type Y/N to continue!")
            choice = input()
            if choice == "Y" or choice == "y":
                with open(CONFIG_FILE, "w") as f:
                    tomlkit.dump({"commands": {}}, f)
                break
            else:
                break
    else:
        with open(CONFIG_FILE, "w") as f:
            tomlkit.dump({"commands": {}}, f)


# : standardize messages
@cli.command()
@click.argument("name")
@click.argument("description")
def add(name, description):
    if not os.path.exists(CONFIG_FILE):
        print("Grimoire needs to be created with command 'new'!")
    try:
        with open(CONFIG_FILE, "r") as f:
            doc = tomlkit.load(f)
    except tomlkit.exceptions.ParseError:
        print("Grimoire unreadable, the text has been corrupted!")
        return
    # : fix this except block

    try:
        entry = tomlkit.table()
        entry.add("description", description)

        doc["commands"].add(name, entry)
        with open(CONFIG_FILE, "w") as f:
            tomlkit.dump(doc, f)
    except Exception:
        print("That spell is already known!")


# : standardize messages
@cli.command()
@click.argument("name")
def remove(name):
    if not os.path.exists(CONFIG_FILE):
        print("Create a grimoire first with command 'new'!")
        return
    try:
        with open(CONFIG_FILE, "r") as f:
            doc = tomlkit.load(f)
    except tomlkit.exceptions.ParseError:
        print("Grimoire unreadable, the text has been corrupted!")
        return

    if name in doc["commands"]:
        doc["commands"].pop(name)
        with open(CONFIG_FILE, "w") as f:
            tomlkit.dump(doc, f)
    #  still writes if unable to locate name


if __name__ == "__main__":
    cli()
