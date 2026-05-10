import os

import click
import tomlkit


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print("Dummy behavior")


@cli.command()
def new():
    config_dir = os.path.expanduser("~/Code/python/hexgrim/config/")
    config_file = os.path.join(config_dir, "hexgrim.toml")
    os.makedirs(config_dir, exist_ok=True)

    if os.path.exists(config_file):
        while True:
            print("Are you sure you wish to reset saved data?")
            print("Type Y/N to continue")
            choice = input()
            if choice == "Y" or "y":
                with open(config_file, "w") as f:
                    tomlkit.dump({"commands": {}}, f)
                print("Saved data cleared!")
                break
            else:
                print("Saved data retained")
                break
    else:
        with open(config_file, "w") as f:
            tomlkit.dump({"commands": {}}, f)


if __name__ == "__main__":
    cli()
