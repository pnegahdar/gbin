import sys

import click

from gbin import GBin


_gbins = None


def run(cmd_name, args=None, always_exit=False, exit_if_failed=True):
    """Run this command"""
    global _gbins
    if not _gbins:
        _gbins = GBin().get_bins()
    if cmd_name not in _gbins:
        click.echo(click.style("No command {}".format(cmd_name), fg='red'))
    return _gbins[cmd_name].execute(args=args, always_exit=always_exit,
                                    exit_if_failed=exit_if_failed)


def list_commands():
    global _gbins
    if not _gbins:
        _gbins = GBin().get_bins()
    indent = " " * 4
    print "Commands:"
    for each in sorted(_gbins.keys()):
        print indent, each


def print_version():
    """Print the inenv version"""
    print '0.2.3'


def run_cli():
    args = sys.argv
    if len(args) == 1:
        list_commands()
        exit(0)
    gbin_command = args[1]
    rest_args = args[2:]
    if gbin_command == 'version':
        print_version()
    else:
        run(gbin_command, rest_args, always_exit=True)


if __name__ == '__main__':
    run_cli()




