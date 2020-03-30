import os
import smtplib, ssl
import socket
from datetime import datetime

from mysqlbackupcfg import config

# get configuration parameters
db_to_backup = config['db_to_backup']
export_dir = config['export_dir']
mail_server = config['mail_server']
mail_server_port = config['mail_server_port']
mail_server_user = config['mail_server_user']
mail_server_password = config['mail_server_password']
mail_from = config['mail_from']
mail_to = config['mail_to']

# prepare error message
error_messages = []

# backup dbs
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
        today = datetime.today()
        dump_name = today.strftime('%y%m%d') + '_' + server + '_' + db_name
        # dump db
        print(dump_name)





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


