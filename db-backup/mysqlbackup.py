import os
import smtplib
import ssl
import socket
from datetime import date, datetime
from shutil import copyfile

from mysqlbackupcfg import config

# get configuration parameters
db_to_backup = config['db_to_backup']
export_dir = config['export_dir']
filename_prefix = config['filename_prefix']
backup_file_history = config['backup_file_history']
weekly_backup = config['weekly_backup']
monthly_backup = config['monthly_backup']
yearly_backup = config['yearly_backup']
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
    current_date = date.today()
    for item in os.listdir(export_dir):
        # check dir content
        item_path = export_dir + '/' + item
        if (os.path.isfile(item_path)):
            # is a file
            if (item.find('_daily-' + filename_prefix + '_') != -1):
                # is a mysql daily backup file
                file_date = date.fromtimestamp(os.path.getctime(item_path))
                if ((current_date - file_date).days > backup_file_history):
                    # the file is old, remove it
                    os.remove(item_path)
            if (current_date.weekday() == 6 and item.find('_weekly-' + filename_prefix + '_') != -1):
                # the weekly file is old, remove it
                os.remove(item_path)
            if (current_date.day == 1 and item.find('_monthly-' + filename_prefix + '_') != -1):
                # the monthly file is old, remove it
                os.remove(item_path)
            if (current_date.day == 1 and current_date.month == 1 and item.find('_yearly-' + filename_prefix + '_') != -1):
                # the yearly file is old, remove it
                os.remove(item_path)    # backup dbs ####
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
            dump_name = start_time.strftime('%Y%m%d') + '_daily-' + filename_prefix + '_' + server + '_' + db_name + '.sql.gz'
            log_name = start_time.strftime('%Y%m%d') + '__daily-' + filename_prefix + '_' + server + '_' + db_name + '.log'
            # dump db
            result = os.system('mysqldump -u ' + user + ' -p' + password + ' -h ' + server + ' -P ' + port + ' ' +
                               db_name + ' 2> ' + export_dir + '/' + log_name + ' | gzip > ' + export_dir + '/' + dump_name)
            # prepare result message
            end_time = datetime.now()
            message = 'Backup del db ' + db_name + ' dal server ' + server + '.'
            if result != 0:
                # error
                esito = 'ERRORE!!!'
                detail_messages.append(message + ' ERRORE!!!!')
            else:
                # success
                # check log file
                log_size = os.path.getsize(export_dir + '/' + log_name)
                if log_size > 0:
                    # error
                    esito = 'ERRORE!!!'
                    detail_messages.append(message + ' ERRORE!!!! Controllare file di log.')
                else:
                    esito = 'OK'
                    detail_messages.append(message + ' OK!')
                    if (weekly_backup == True and current_date.weekday() == 6):
                        # copy to weekly file
                        copyfile(dump_name, start_time.strftime('%Y%m%d') + '_weekly-' + filename_prefix + '_' + server + '_' + db_name + '.sql.gz')
                    if (monthly_backup == True and current_date.day == 1):
                        # copy to monthly file
                        copyfile(dump_name, start_time.strftime('%Y%m%d') + 'monthly-' + filename_prefix + '_' + server + '_' + db_name + '.sql.gz')
                    if (yearly_backup == True and current_date.day == 1 and current_date.month == 1):
                        # copy to yearly file
                        copyfile(dump_name, start_time.strftime('%Y%m%d') + 'yearly-' + filename_prefix + '_' + server + '_' + db_name + '.sql.gz')
            detail_messages.append('Inizio: ' + start_time.strftime('%d-%m-%Y %H:%M') + ' - Fine: ' + end_time.strftime('%d-%m-%Y %H:%M') +
                                   ' - Dimensione: ' + str(os.path.getsize(export_dir + '/' + dump_name)) + '\n')
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
        message.append('From: ' + mail_from)
        message.append('To: ' + ', '.join(mail_to))
        message.append('Backup dei database del server ' + socket.gethostname() + '\n')
        message += detail_messages
        message.append('')
        # send email
        server.sendmail(mail_from, mail_to, '\n'.join(message))
