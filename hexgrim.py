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
# TODO: standardize messages
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


# TODO: standardize messages
# TODO: Add feedback for when a fresh file is made
# NOTE: Possibly change confirmation dialog
@cli.command()
def new():
    config_dir = os.path.expanduser("~/.config/hexgrim/")
    os.makedirs(config_dir, exist_ok=True)

    if os.path.exists(CONFIG_FILE):
        while True:
            print("Are you sure you wish to reset saved data?")
            print("Type Y/N to continue")
            choice = input()
            if choice == "Y" or choice == "y":
                with open(CONFIG_FILE, "w") as f:
                    tomlkit.dump({"commands": {}}, f)
                print("Saved data cleared!")
                break
            else:
                print("Saved data retained")
                break
    else:
        with open(CONFIG_FILE, "w") as f:
            tomlkit.dump({"commands": {}}, f)


# TODO: standardize messages
@cli.command()
@click.argument("name")
@click.argument("description")
def add(name, description):
    try:
        with open(CONFIG_FILE, "r") as f:
            doc = tomlkit.load(f)
    except Exception:
        print("Unable to open grimoire. Initialize with 'new' command!")
        return
    # TODO: fix this except block

    try:
        entry = tomlkit.table()
        entry.add("description", description)

        doc["commands"].add(name, entry)
        with open(CONFIG_FILE, "w") as f:
            tomlkit.dump(doc, f)
        print("Entry added to grimoire")
    except Exception:
        print("That's already in the grimoire!")


# TODO: standardize messages
@cli.command()
@click.argument("name")
def remove(name):

    try:
        with open(CONFIG_FILE, "r") as f:
            doc = tomlkit.load(f)
    except Exception:
        print("Unable to open grimoire")
        return

    if name in doc["commands"]:
        doc["commands"].pop(name)
        print("Entry removed from grimoire")
    # BUG still writes if unable to locate name
    with open(CONFIG_FILE, "w") as f:
        tomlkit.dump(doc, f)


if __name__ == "__main__":
    cli()
