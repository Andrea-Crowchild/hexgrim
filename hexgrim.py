import os

import click
import tomlkit


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print("Dummy behavior")


@cli.command
def new():
    config_dir = os.path.expanduser("~/Code/python/hexgrim/")
    config_file = os.path.join(config_dir, "hexgrim.toml")
    os.makedirs(config_dir, exist_ok=True)

    if os.path.exists(config_file):
        print("Are you sure you want to delete all data? y/n")
        choice = input()
        if choice == "y":
            with open(config_file, "w") as f:
                f.write("")
        else:
            print("Data retained")


if __name__ == "__main__":
    cli()
