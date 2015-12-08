import subprocess
import os


def get_git_command(git_dir):
    """
    Grabs the git command with the --work-tree and --git-dir args set
    :rtype: list
    """
    dot_git_dir = os.path.join(git_dir, '.git')
    return ['git', '--git-dir', dot_git_dir, '--work-tree', git_dir]


def is_git_dir(git_dir):
    """Returns whether its a git directory or not
    :rtype: bool
    """
    try:
        subprocess.check_call(get_git_command(git_dir) + ['rev-parse', '--git-dir'],
                              stdout=open(os.devnull, 'wb'))
        return True
    except subprocess.CalledProcessError:
        return False


def has_git_cmd():
    """Returns whether you have the `git` command available or not
    :rtype: bool
    """
    return bool(subprocess.check_output(['which', 'git']))


def git_find_files(git_dir, match):
    """ Basically git ls-files
    :rtype: list
    """
    try:
        tracked = get_git_command(git_dir) + ['ls-files', '--full-name', git_dir, '|', 'grep',
                                              match]
        tracked_gbins = subprocess.check_output(' '.join(tracked), shell=True).splitlines()
    except subprocess.CalledProcessError:
        tracked_gbins = []
    try:
        untracked = get_git_command(git_dir) + ['ls-files', '--full-name', '--exclude-standard',
                                                '--others', git_dir, '|', 'grep', match]

        untracked_gbins = subprocess.check_output(' '.join(untracked), shell=True).splitlines()
    except subprocess.CalledProcessError:
        untracked_gbins = []
    return tracked_gbins + untracked_gbins
