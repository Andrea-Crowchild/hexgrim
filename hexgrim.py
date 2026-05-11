import os

import click
import tomlkit

config_dir = os.path.expanduser("~/.config/hexgrim/")
CONFIG_FILE = os.path.join(config_dir, "hexgrim.toml")


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        with open(CONFIG_FILE, "r") as f:
            doc = tomlkit.load(f)

        for name, desc in sorted(doc["commands"].items()):
            print(name, ":", desc["description"])


@cli.command()
@click.argument("name")
@click.argument("description")
def add(name, description):
    with open(CONFIG_FILE, "r") as f:
        doc = tomlkit.load(f)
    try:
        entry = tomlkit.table()
        entry.add("description", description)

        doc["commands"].add(name, entry)
        with open(CONFIG_FILE, "w") as f:
            tomlkit.dump(doc, f)
        print("Entry added to grimoire")
    except:
        print("That's already in the grimoire!")


@cli.command()
def new():
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


@cli.command()
@click.argument("name")
def remove(name):

    try:
        with open(CONFIG_FILE, "r") as f:
            doc = tomlkit.load(f)
    except:
        print("Unable to read grimoire!")

    if name in doc["commands"]:
        doc["commands"].pop(name)
    else:
        print(f"{name} not found in grimoire!")

    with open(CONFIG_FILE, "w") as f:
        tomlkit.dump(doc, f)


if __name__ == "__main__":
    cli()
