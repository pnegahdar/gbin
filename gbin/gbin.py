import os
import collections
import re
import subprocess
import sys

from inenv.inenv import InenvManager

from utils import has_git_cmd, is_git_dir, git_find_files


shebang_map = {
    '.js': ['/usr/bin/env', 'node'],
    '.py': ['/usr/bin/env', 'python'],
    '.sh': ['/usr/bin/env', 'bash']
}
RECURSION_LIMIT = 100
GBIN_DIRS = 'gbin'
GBIN_FILE_GLOB = 'gbin/'
GBIN_EXCLUED_FN = {'__init__.py'}
GBIN_EXCLUDE_EXT = {'.pyc'}
GBIN_DOC_LINE_LIMIT = 2  # Number of lines to check for a doc
REGEX_DOC_RE = re.compile(r'^[\-;#\/\s}{]+["\']([^"\']+)["\']$')


class GbinException(Exception):
    pass


class GBin(object):
    def __init__(self, git_dir=None, glob=GBIN_FILE_GLOB, exclude_extensions=GBIN_EXCLUDE_EXT,
                 excluded_fn=GBIN_EXCLUED_FN, inenv_manager=None):
        if not has_git_cmd():
            raise GbinException("No git command found.")
        git_dir = git_dir or self.closes_git_dir()
        if not is_git_dir(git_dir):
            raise GbinException("{} is not a git directory".format(git_dir))
        self._glob = glob
        self._ext_ex = exclude_extensions
        self._fn_ex = excluded_fn
        self.git_dir = git_dir
        self.inenv_manager = inenv_manager

    def get_bins(self):
        bins = []
        potential_files = git_find_files(git_dir=self.git_dir, match=self._glob)
        for fn in potential_files:
            ext = os.path.splitext(fn)[1]
            if ext and ext in self._ext_ex:
                continue
            if os.path.basename(fn) in GBIN_EXCLUED_FN:
                continue
            full_path = os.path.join(self.git_dir, fn)
            bins.append(Bin(full_path, self.inenv_manager))
        dups = [item for item, count in
                collections.Counter([bin.pretty_name for bin in bins]).items() if count > 1]
        if dups:
            raise GbinException("Found duplicate commands: {}".format(', '.join(dups)))
        return {bin.pretty_name: bin for bin in bins}

    def closes_git_dir(self):
        directory = os.path.abspath(os.path.curdir)
        x = RECURSION_LIMIT
        while x > 0:
            git_path = os.path.join(directory, '.git')
            if not os.access(directory, os.W_OK):
                raise GbinException(
                    "Unable to find git directory. Lost permissions walking up to {}. ".format(
                        directory))
            if os.path.isdir(git_path):
                return directory
            parent_dir = os.path.realpath(os.path.join(directory, '..'))
            if parent_dir == directory:
                raise GbinException(
                    "Walked all the way up to {} and was unable to find git dir".format(parent_dir))
            directory = parent_dir
            x -= 1
        raise GbinException("Recursion limit exceeded unable to find git dir")


class Bin(object):
    def __init__(self, abs_path, inenv_manager=None):
        self.inenv_manager = inenv_manager
        self._abs_path = abs_path
        self._inenv_name = None
        self._closest_venv = None
        self._closest_prepped_venv = None
        self._pretty_name = None
        self._doc = None

    @property
    def abs_path(self):
        return self._abs_path


    def path_relative_to(self, start_path):
        pass

    @property
    def closest_venv(self):
        if not self._closest_venv:
            inenv = self.inenv_manager or InenvManager(
                search_start_dir=os.path.dirname(self._abs_path))
            roots = {v['root']: k for k, v in inenv.registered_venvs.items()}
            self.inenv_manager = inenv
            cur_dir = os.path.dirname(os.path.dirname(self._abs_path))
            while True:
                if cur_dir in roots:
                    self._closest_venv = inenv.get_venv(roots[cur_dir])
                    return self._closest_venv
                os.path.dirname(cur_dir)
                next_dir = os.path.dirname(cur_dir)
                if next_dir == cur_dir:
                    break
                cur_dir = next_dir
        return self._closest_venv

    @property
    def closest_prepped_venv(self):
        if os.isatty(1):
            stdout = sys.stdout
        else:
            stdout = open(os.devnull, "w")
        if not self._closest_prepped_venv:
            venv = self.closest_venv
            self._closest_prepped_venv = self.inenv_manager.get_prepped_venv(venv.venv_name,
                                                                             stdout=stdout)
        return self._closest_prepped_venv

    def execute(self, args=None, always_exit=False, exit_if_failed=True, stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr):
        cmd = []
        is_exec = os.access(self._abs_path, os.X_OK)
        ext = os.path.splitext(self._abs_path)[1]
        if not is_exec:
            if ext in shebang_map:
                cmd += shebang_map[ext]
            else:
                raise GbinException(
                    "File {} is not an executable and the extension {} is unknown".format(
                        self._abs_path, ext))
        cmd.append(self._abs_path)
        if args:
            cmd = cmd + list(args)
        if self.closest_venv:
            process = self.closest_prepped_venv.run(cmd, always_exit=always_exit,
                                                    exit_if_failed=exit_if_failed, stdin=stdin,
                                                    stdout=stdout, stderr=stderr)
        else:
            process = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)

            exit_code = process.wait()
            if always_exit:
                sys.exit(exit_code)
            if exit_if_failed and exit_code != 0:
                sys.exit(exit_code)
        return process

    @property
    def pretty_name(self):
        if not self._pretty_name:
            parts = []
            if self.closest_venv:
                parts.append(self.closest_venv.venv_name)
            parts.append(os.path.splitext(os.path.basename(self._abs_path))[0])
            self._pretty_name = '.'.join(parts)
        return self._pretty_name

    @property
    def doc(self):
        if self._doc is None:
            with open(self._abs_path) as exc_file:
                first_lines = [exc_file.readline() for _ in range(GBIN_DOC_LINE_LIMIT)]
                for line in first_lines:
                    results = REGEX_DOC_RE.findall(line)
                    if results:
                        self._doc = results[0]
                        break
            if not self._doc:
                self._doc = ''
        return self._doc
