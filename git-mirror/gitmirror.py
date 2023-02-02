import sys
import smtplib
import ssl
import socket
from pathlib import Path
from datetime import date, datetime

import git

from gitmirrorcfg import config

# get command line parameters
only_new = False
send_mail = False
for i in range(len(sys.argv) - 1):
    if sys.argv[i + 1] == '--help':
        print('Git Mirror - GIT repository replica')
        print('Use gitmirrorcfg.py for configuration')
        print('Usage: python gitmirror.py [--only-new] [--send-mail] [--help]')
        print('\t--only-new: only create and download new repository (not on local disk)')
        print('\t--send-mail: send a report email at the end of the synchronization')
        sys.exit(0)
    if sys.argv[i + 1] == '--only-new':
        only_new = True
    if sys.argv[i + 1] == '--send-mail':
        send_mail = True

# import parameters
git_exe = config['git_executable_path']
repositories = config['repositories']
mail_server = config['mail_server']
mail_server_port = config['mail_server_port']
mail_server_user = config['mail_server_user']
mail_server_password = config['mail_server_password']
mail_from = config['mail_from']
mail_to = config['mail_to']

# prepare result message
detail_messages = []
esito = 'OK'

# sync repos
start_time = datetime.now()
for repository in repositories:
    # get repository data
    name = repository['name']
    path = repository['path']
    source = repository['source']
    destination = repository['destination']
    repoPath = path + os.path.sep + name
    print('Repo: ' + name, end='', flush=True)
    detail_message = 'Repo: ' + name
    is_new = False
    # create path
    path_dir = Path(path)
    path_dir.mkdir(parents=True, exist_ok=True)
    try:
        if (not Path(repoPath).exists()):
            # path not exist
            is_new = True
            print(' - Clone: ', end='', flush=True)
            detail_message += ' - Clone: '
            # clone repository
            git.Git(path).clone(source, ['--mirror', name])
            # clone executed
            print('OK', end='', flush=True)
            detail_message += 'OK'
            print(' - Config: ', end='', flush=True)
            detail_message += ' - Config: '
            # set new destination
            if destination.lower() != 'off':
                repo = git.Repo(repoPath)
                repo.remotes.origin.set_url(destination, ['--push'])
                print('OK', end='', flush=True)
                detail_message += 'OK'
            else:
                print('OFF', end='', flush=True)
                detail_message += 'OFF'
        # fetch from source
        if (not only_new or (only_new and is_new)):
            print(' - Fetch: ', end='', flush=True)
            detail_message += ' - Fetch: '
            repo = git.Repo(repoPath)
            origin = repo.remotes.origin
            response = origin.fetch()[0]
            if not (response.flags & git.FetchInfo.ERROR or response.flags & git.FetchInfo.REJECTED):
                # fetch executed
                print('OK', end='', flush=True)
                detail_message += 'OK'
                print(' - Push: ', end='', flush=True)
                detail_message += ' - Push: '
                if destination.lower() != 'off':
                    response = origin.push()[0]
                    if not (response.flags & git.PushInfo.ERROR or response.flags & git.PushInfo.REJECTED or response.flags & git.PushInfo.REMOTE_FAILURE or response.flags & git.PushInfo.REMOTE_REJECTED):
                        print('OK')
                        detail_message += 'OK'
                    else:
                        raise IOError()
                else:
                    print('OFF')
                    detail_message += 'OFF'
            else:
                raise IOError()
        else:
            print(' - Excluded: OK')
            detail_message += ' - Excluded: OK'
    except:
        print('ERROR: ', sys.exc_info()[0])
        detail_message += ' - ERROR'
        esito = 'ERROR'
    # adde message to messages list
    detail_messages.append(detail_message)

# send email ####
if send_mail:
    # initialize ssl context
    context = ssl.create_default_context()
    # send email
    with smtplib.SMTP_SSL(mail_server, mail_server_port, context=context) as server:
        # log into server
        server.login(mail_server_user, mail_server_password)
        # prepare mail message
        message = []
        message.append('Subject: [' + socket.gethostname() + '] Backup dei repo GIT - Esito: ' + esito)
        message.append('From: ' + mail_from)
        message.append('To: ' + ', '.join(mail_to))
        message.append('Backup dei repositiry GIT sul server ' + socket.gethostname() + '\n')
        message += detail_messages
        message.append('')
        # send email
        server.sendmail(mail_from, mail_to, '\n'.join(message))
