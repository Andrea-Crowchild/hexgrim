#!/usr/bin/env python3

import os

import click
import tomlkit

CONFIG_FILE = os.path.expanduser("~/.config/hexgrim/hexgrim.toml")


# TODO: Better help doc
# TODO: Add ability to save and backup toml
# : Ability to edit spells
# TODO: good comments necessary
# TODO: Make exceptions better
# TODO: Cleanup
# TODO: Testing
# : Fix Spacing
# : standardize messages
# TODO Prep for packaging
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Hexgrim - a personal command reference tool"""
    if ctx.invoked_subcommand is None:
        with open(CONFIG_FILE, "r") as f:
            doc = tomlkit.load(f)

        width = max(len(name) for name in doc["commands"]) + 2
        for name, desc in sorted(doc["commands"].items()):
            print(name.ljust(width), ":", desc["description"])


# : standardize messages
# : Add feedback for when a fresh file is made
# NOTE: Possibly change confirmation dialog
@cli.command()
def new():
    """Create a new grimoire or purge the file and start anew"""
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
    """Add an entry to the grimoire"""
    if not os.path.exists(CONFIG_FILE):
        print("Grimoire needs to be created with command 'new'!")
        return
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


@cli.command()
@click.argument("name")
@click.argument("description")
def edit(name, description):
    """Edit an entry in the grimoire"""
    if not os.path.exists(CONFIG_FILE):
        print("Grimoire needs to be created with command 'new'!")
        return
    try:
        with open(CONFIG_FILE, "r") as f:
            doc = tomlkit.load(f)
    except tomlkit.exceptions.ParseError:
        print("Grimoire unreadable, the text has been corrupted!")
        return

    if name not in doc["commands"]:
        print("Unknown spell, use add to add a new spell!")
        return
    entry = tomlkit.table()
    entry.add("description", description)
    doc["commands"][name] = entry
    with open(CONFIG_FILE, "w") as f:
        tomlkit.dump(doc, f)


# : standardize messages
@cli.command()
@click.argument("name")
def remove(name):
    """Remove an entry from the grimoire"""
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


@cli.command()
@click.argument("location")
def save(location):
    pass


if __name__ == "__main__":
    cli()
