import subprocess

from gitmirrorcfg import config

# import parameters
git_exe = config['git_executable_path']
repositories = config['repositories']

# git mirroring commands
source_fetch = [git_exe, 'fetch', '-p', 'origin']
destination_push = [git_exe, 'push', '--mirror']

# sync repos
for repository in repositories:
    # get repository data
    name = repository['name']
    path = repository['path']
    # fetch from source
    print('Repo: ' + name + ' - Fetch: ', end='', flush=True)
    git = subprocess.Popen(source_fetch, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    (git_status, git_error) = git.communicate()
    if git.poll() == 0:
        # fetch executed
        print('OK', end='', flush=True)
        print(' - Push: ', end='', flush=True)
        git = subprocess.Popen(destination_push, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        (git_status, git_error) = git.communicate()
        if git.poll() == 0:
            print('OK')