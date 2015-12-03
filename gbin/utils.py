import subprocess
import os


def get_git_command(git_dir):
    """
    Grabs the git command with the --work-tree and --git-dir args set
    :rtype: list
    """
    dot_git_dir = os.path.join(git_dir, '.git')
    return ['git', '--git-dir', dot_git_dir , '--work-tree', git_dir]


def is_git_dir(git_dir):
    """Returns whether its a git directory or not
    :rtype: bool
    """
    try:
        subprocess.check_call(get_git_command(git_dir) + ['rev-parse', '--git-dir'])
        return True
    except subprocess.CalledProcessError:
        return False


def has_git_cmd():
    """Returns whether you have the `git` command available or not
    :rtype: bool
    """
    return bool(subprocess.check_output(['which', 'git']))


def git_find_files(git_dir, match=None):
    """ Basically git ls-files
    :rtype: list
    """
    results = subprocess.check_output(get_git_command(git_dir) + filter(None, ['ls-files', match]))
    return results.splitlines()
