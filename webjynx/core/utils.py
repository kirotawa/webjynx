import re
import os
import sys

exp_reg = re.compile(r'[\w|d]{40}')

try:
    import git as _git
except ImportError:
    print "You need to install python-git"
    sys.exit(1)


def log(git, file):
    log = git.log('--pretty=oneline', file)
    log_lines = log.split('\n')

    sha_list = []
    for line in log_lines:
        sha = exp_reg.match(line)
        sha = sha.group()
        msg = line[41:]
        sha_list.append([sha, msg])

    return sha_list


def get_commit_shas(path_file, path_repository):
    temp_path = None
    path = None

    if os.path.isdir(path_repository):
        temp_path = path_repository

        if '.git' in os.listdir(temp_path):
            if os.path.isfile(temp_path+'/'+path_file):
                path = temp_path
            else:
                return "Not a valid file"
        else:
            return "Is not a valid git repository"
    else:
        return "Not a valid directory"

    try:
        git = _git.cmd.Git(path)
        return log(git, path_file)

    except _git.GitCommandError:
        return "error"


def get_patch_file(git, sha):
    return git.format_patch(-1, sha, '--stdout')


def get_patch(sha, repository):
    # We don't need to recheck once a sha comes from a real dir, git and file
    try:
        git = _git.cmd.Git(repository)
        return get_patch_file(git, sha)
    except _git.cmd.GitCommandError:
        return "error"
