import sys

import click
from click.formatting import HelpFormatter

from gbin import GBin, GbinException


_gbins = None


def run(cmd_name, args=None, always_exit=False, exit_if_failed=True):
    """Run this command"""
    global _gbins
    if not _gbins:
        _gbins = GBin().get_bins()
    if cmd_name not in _gbins:
        click.echo(click.style("No command {} try one of these:".format(cmd_name), fg='red'))
        list_commands()
        exit(1)
    return _gbins[cmd_name].execute(args=args, always_exit=always_exit,
                                    exit_if_failed=exit_if_failed)


def list_commands():
    global _gbins
    if not _gbins:
        _gbins = GBin().get_bins()
    formatter = HelpFormatter()
    doc_pairs = [(name, bin.doc) for name, bin in sorted(_gbins.items(), key=lambda x: x[0])]
    with formatter.section('Commands'):
        formatter.write_dl(doc_pairs or [tuple()])
    print formatter.getvalue()


def print_version():
    """Print the inenv version"""
    print '0.2.5'


def run_cli():
    try:
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
    except GbinException as e:
        click.echo(click.style("{}".format(e.message), fg='red'))


if __name__ == '__main__':
    run_cli()




