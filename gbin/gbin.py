import os

from utils import has_git_cmd, is_git_dir, git_find_files


shebang_map = {
    'js': '/usr/bin/env node',
    'py': '/usr/bin/env python'
}

GBIN_DIRS = 'gbin'
GBIN_FILE_GLOB = os.path.join('**', *[GBIN_DIRS, '*'])
GBIN_EXCLUED_FN = ['__init__.py']
GBIN_EXCLUDE_EXT = ['.pyc']


class GbinException(Exception):
    pass


class GBin(object):
    def __init__(self, git_dir, glob=GBIN_FILE_GLOB):
        if not has_git_cmd():
            raise GbinException("No git command found.")
        if not is_git_dir(git_dir):
            raise GbinException("{} is not a git directory".format(git_dir))
        self._glob = glob
        self.git_dir = git_dir

    def get_bins(self):
        potential_files = git_find_files(git_dir=self.git_dir, match=self._glob)



class Bin(object):
    def __init__(self, abs_path):
        self._abs_path = abs_path
        self._inenv_name = None

    @property
    def abs_path(self):
        pass


    def path_relative_to(self, start_path):
        pass

    @property
    def closest_venv(self):
        pass


    def execute(self, quiet=False):
        pass
