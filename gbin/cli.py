import itertools
import os
import sys

import click
from click.formatting import HelpFormatter

from gbin import GBin, GbinException


_gbins = None


def find_cmd(gbins, user_input):
    if user_input in gbins:
        return gbins[user_input]
    sub_matches = [key for key in gbins.keys() if user_input in key.split('.')]
    if len(sub_matches) == 1:
        return gbins[sub_matches[0]]
    elif len(sub_matches) >= 1:
        click.echo(click.style("Multiple results: {}".format(', '.join(sub_matches)), fg='red'))
        exit(1)
    else:
        click.echo(
            click.style("No command {}. Type gbin for full cmd list".format(user_input), fg='red'))
        exit(1)


def run(cmd_name, args=None, always_exit=False, exit_if_failed=True):
    """Run this command"""
    global _gbins
    if not _gbins:
        _gbins = GBin().get_bins()
    cmd = find_cmd(_gbins, cmd_name)
    return cmd.execute(args=args, always_exit=always_exit, exit_if_failed=exit_if_failed)


def list_commands():
    global _gbins
    if not _gbins:
        _gbins = GBin().get_bins()
    formatter = HelpFormatter()
    sorted_bins = [(name, gbin.doc) for name, gbin in sorted(_gbins.items(), key=lambda x: x[0])]
    if os.isatty(1):
        doc_groups = itertools.groupby(sorted_bins, key=lambda x: x[0].split('.')[0])
    else:
        doc_groups = [(None, sorted_bins)]
    with formatter.section(click.style('Commands', fg='green')):
        for group, doc_pairs in doc_groups:
            if group:
                with formatter.section(click.style(group, fg='blue')):
                    formatter.write_dl(doc_pairs or [tuple()])
            else:
                formatter.write_dl(doc_pairs or [tuple()])
    print formatter.getvalue()


def print_version():
    """Print the inenv version"""
    print '0.2.8'


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




