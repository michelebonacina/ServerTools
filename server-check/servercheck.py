import shutil
import smtplib, ssl
import socket

import sys

from servercheckcfg import config

# get configuration parameters
disk_to_check = config['disk_to_check']
disk_used_perc_limit = config['disk_used_perc_limit']
mail_server = config['mail_server']
mail_server_port = config['mail_server_port']
mail_server_user = config['mail_server_user']
mail_server_password = config['mail_server_password']
mail_from = config['mail_from']
mail_to = config['mail_to']

# prepare error message
error_messages = []

# check disks
for disk in disk_to_check:
    # get disk usage
    total, used, free = shutil.disk_usage(disk)
    used_perc = round(used / total * 100)
    # check usage limit
    if used_perc > disk_used_perc_limit:
        # usage over limit
        error_messages.append('Il disco ' + disk + ' e\' occupato al ' + str(used_perc) + '%.')

if len(error_messages) > 0:
    # initialize ssl context
    context = ssl.create_default_context()
    # send email
    with smtplib.SMTP_SSL(mail_server, mail_server_port, context=context) as server:
        # log into server
        server.login(mail_server_user, mail_server_password)
        # prepare mail message
        message = []
        message.append('Subject: [' + socket.gethostname() + '] Stato occupazione dei dischi')
        message.append('Controllo dello spazio su disco del server ' + socket.gethostname())
        message += error_messages
        message.append('')

        # send email
        server.sendmail(mail_from, mail_to, '\n'.join(message))


