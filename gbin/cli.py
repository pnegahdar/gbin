import copy

import click

from gbin import GBin
import version


_gbins = None


@click.group(name='gbin')
@click.version_option(version=version.__version__)
def main_cli():
    pass


@click.option('--cmd-name', default=None)
@click.command()
def run(cmd_name):
    """Run this command"""
    global _gbins
    if not _gbins:
        _gbins = GBin().get_bins()
    if cmd_name not in _gbins:
        click.echo(click.style("No command {}".format(cmd_name), fg='red'))
    _gbins[cmd_name].execute()


@main_cli.command('version')
def print_version():
    """Print the inenv version"""
    print version.__version__


def run_cli():
    global _gbins
    if not _gbins:
        _gbins = GBin().get_bins()
    for bin in _gbins.keys():
        new_switch = copy.deepcopy(run)
        for param in new_switch.params:
            if param.name == 'cmd_name':
                param.default = bin
        main_cli.add_command(new_switch, name=bin)
    main_cli(obj={}, prog_name="gbin")


if __name__ == '__main__':
    run_cli()




