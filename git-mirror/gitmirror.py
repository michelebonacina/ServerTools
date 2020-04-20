import subprocess
import sys
import os

from gitmirrorcfg import config

# get command line parameters
only_new = False

for i in range(len(sys.argv) - 1):
    if sys.argv[i + 1] == '--only-new':
        only_new = True

# import parameters
git_exe = config['git_executable_path']
repositories = config['repositories']

# git mirroring commands
source_clone = [git_exe, 'clone', '--mirror', '', '']
source_destination = [git_exe, 'remote', 'set-url', '--push', 'origin', '']
source_fetch = [git_exe, 'fetch', '-p', 'origin']
destination_push = [git_exe, 'push', '--mirror']

# sync repos
for repository in repositories:
    # get repository data
    name = repository['name']
    path = repository['path']
    path_project = path + '/' + name
    source = repository['source']
    destination = repository['destination']
    print('Repo: ' + name, end='', flush=True)
    is_new = False
    try:
        if (not os.path.exists(path + '/' + name)):
            # path not exist
            is_new = True
            print(' - Clone: ', end='', flush=True)
            # clone repository
            source_clone[3] = source
            source_clone[4] = name
            git = subprocess.Popen(
                source_clone, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            (git_status, git_error) = git.communicate()
            if git.poll() == 0:
                # clone executed
                print('OK', end='', flush=True)
                print(' - Config: ', end='', flush=True)
                # set new destination
                if destination.lower() != 'off':
                    source_destination[5] = destination
                    git = subprocess.Popen(source_destination, cwd=path_project,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    (git_status, git_error) = git.communicate()
                    if git.poll() == 0:
                        print('OK', end='', flush=True)
                    else:
                        raise IOError()
                else:
                    print('OFF', end='', flush=True)
            else:
                raise IOError()
        # fetch from source
        if (not only_new or (only_new and is_new)):
            print(' - Fetch: ', end='', flush=True)
            git = subprocess.Popen(source_fetch, cwd=path_project,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            (git_status, git_error) = git.communicate()
            if git.poll() == 0:
                # fetch executed
                print('OK', end='', flush=True)
                print(' - Push: ', end='', flush=True)
                if destination.lower() != 'off':
                    git = subprocess.Popen(destination_push, cwd=path_project,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    (git_status, git_error) = git.communicate()
                    if git.poll() == 0:
                        print('OK')
                    else:
                        raise IOError()
                else:
                    print('OFF')
            else:
                raise IOError()
        else:
            print(' - Excluded: OK')
    except:
        print('ERROR: ', sys.exc_info()[0])
