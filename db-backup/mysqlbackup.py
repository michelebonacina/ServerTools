import os
import smtplib, ssl
import socket
from datetime import datetime

import sys

from mysqlbackupcfg import config

# get configuration parameters
db_to_backup = config['db_to_backup']
export_dir = config['export_dir']
filename_prefix = config['filename_prefix']
backup_file_history = config['backup_file_history']
mail_server = config['mail_server']
mail_server_port = config['mail_server_port']
mail_server_user = config['mail_server_user']
mail_server_password = config['mail_server_password']
mail_from = config['mail_from']
mail_to = config['mail_to']

# prepare result message
detail_messages = []
esito = ''

if (os.path.exists(export_dir) and os.path.isdir(export_dir)):
    # export dir exists
    # remove old file from export dir ####
    current_date = int(datetime.now().strftime('%Y%m%d'))
    for item in os.listdir(export_dir):
        # check dir content
        item_path = export_dir + '/' + item
        if (os.path.isfile(item_path)):
            # is a file
            if (item.find('_' + filename_prefix + '_') != -1):
                # is a mysql backup file
                backup_date_str = item[:8]
                if (backup_date_str.isdecimal()):
                    # is the backup date
                    backup_date = int(backup_date_str)
                    if (backup_date < current_date - backup_file_history):
                        # the file is old, remove it
                        os.remove(item_path)
    # backup dbs ####
    for db in db_to_backup:
        # get db data
        server = db['server']
        port = db['port']
        user = db['user']
        password = db['password']
        db_names = db['db_names']
        # backup db
        for db_name in db_names:
            # prepare dump name
            start_time = datetime.now()
            dump_name = start_time.strftime('%Y%m%d') + '_' + filename_prefix + '_' + server + '_' + db_name + '.sql.gz'
            # dump db
            result = os.system('mysqldump -u ' + user + ' -p' + password + ' -h ' + server + ' -P ' + port + ' ' + db_name + ' | gzip > ' + export_dir + '/' + dump_name)
            # prepare result message
            end_time = datetime.now()
            message = 'Backup del db ' + db_name + ' dal server ' + server + '.'
            if result != 0:
                # error
                esito = 'ERRORE!!!'
                detail_messages.append(message + ' ERRORE!!!!')
            else:
                # success
                esito = 'OK'
                detail_messages.append(message + ' OK!')
            detail_messages.append('Inizio: ' + start_time.strftime('%d-%m-%Y %H:%M') + ' - Fine: ' + end_time.strftime('%d-%m-%Y %H:%M') + ' - Dimensione: ' + str(os.path.getsize(export_dir + '/' + dump_name)) + '\n')
else:
    # export dir not finded
    esito = 'ERRORE!!!'
    detail_messages.append('La directory di export ' + export_dir + ' non esiste.')

# send email ####
if len(detail_messages) > 0:
    # initialize ssl context
    context = ssl.create_default_context()
    # send email
    with smtplib.SMTP_SSL(mail_server, mail_server_port, context=context) as server:
        # log into server
        server.login(mail_server_user, mail_server_password)
        # prepare mail message
        message = []
        message.append('Subject: [' + socket.gethostname() + '] Backup dei database - Esito: ' + esito)
        message.append('Backup dei database del server ' + socket.gethostname() + '\n')
        message += detail_messages
        message.append('')
        # send email
        server.sendmail(mail_from, mail_to, '\n'.join(message))
