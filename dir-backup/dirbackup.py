import os
import smtplib
import ssl
import socket
from zipfile import ZipFile
from datetime import date, datetime
from shutil import copyfile, make_archive

from dirbackupcfg import config

# get configuration parameters
dir_to_backup = config['dir_to_backup']
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

def make_zip(path, filename):
    # get global variables
    global export_dir, filename_prefix
    global weekly_backup, monthly_backup, yearly_backup
    global esito, detail_messages

    # prepare dump name
    start_time = datetime.now()
    dump_name = start_time.strftime('%Y%m%d') + '_daily-' + filename_prefix + '_' + filename 
    # zip dir
    dump_name = make_archive(export_dir + '/' + dump_name, 'zip', path)
    # prepare result message
    end_time = datetime.now()
    message = 'Backup della dir ' + path + ' nel file ' + dump_name + '.'
    # success
    esito = 'OK'
    detail_messages.append(message + ' OK!')
    if (weekly_backup == True and current_date.weekday() == 6):
        # copy to weekly file
        copyfile(dump_name, export_dir + '/' + start_time.strftime('%Y%m%d') + '_weekly-' + filename_prefix + '_' + filename + '.zip')
    if (monthly_backup == True and current_date.day == 1):
        # copy to monthly file
        copyfile(dump_name, start_time.strftime('%Y%m%d') + 'monthly-' + filename_prefix + '_' + filename + '.zip')
    if (yearly_backup == True and current_date.day == 1 and current_date.month == 1):
        # copy to yearly file
        copyfile(dump_name, start_time.strftime('%Y%m%d') + 'yearly-' + filename_prefix + '_' + filename + '.zip')
    detail_messages.append('Inizio: ' + start_time.strftime('%d-%m-%Y %H:%M') + ' - Fine: ' + end_time.strftime('%d-%m-%Y %H:%M') +
                            ' - Dimensione: ' + str(os.path.getsize(dump_name)) + '\n')

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
                os.remove(item_path)    
    # backup dirs ####
    for dir_data in dir_to_backup:
        # get dir data
        path = dir_data['path']
        filename = dir_data['filename']
        split_dir = dir_data['split_dir']
        # check directory split
        if (split_dir) :
            # zip single sub directory
            # extract sub directory list and file in specified path
            subdir_list = []
            filename_list = []
            for (dirpath, dirnames, filenames) in os.walk(path):
                subdir_list.extend(dirnames)
                filename_list.extend(filenames)
                break           
            # create temporary directory for single files
            if (len(filenames) > 0):
                # prepare dump name
                start_time = datetime.now()
                dump_name = start_time.strftime('%Y%m%d') + '_daily-' + filename_prefix + '_' + filename + '.zip'
                # zip files in dir
                zip_file = ZipFile(dump_name, 'w')
                for filename_dir in filenames:
                    zip_file.write(path + '/' + filename_dir, filename_dir);
                # prepare result message
                end_time = datetime.now()
                message = 'Backup della dir ' + path + ' nel file ' + dump_name + '.'
                # success
                esito = 'OK'
                detail_messages.append(message + ' OK!')
                if (weekly_backup == True and current_date.weekday() == 6):
                    # copy to weekly file
                    copyfile(dump_name, export_dir + '/' + start_time.strftime('%Y%m%d') + '_weekly-' + filename_prefix + '_' + filename + '.zip')
                if (monthly_backup == True and current_date.day == 1):
                    # copy to monthly file
                    copyfile(dump_name, start_time.strftime('%Y%m%d') + 'monthly-' + filename_prefix + '_' + filename + '.zip')
                if (yearly_backup == True and current_date.day == 1 and current_date.month == 1):
                    # copy to yearly file
                    copyfile(dump_name, start_time.strftime('%Y%m%d') + 'yearly-' + filename_prefix + '_' + filename + '.zip')
                detail_messages.append('Inizio: ' + start_time.strftime('%d-%m-%Y %H:%M') + ' - Fine: ' + end_time.strftime('%d-%m-%Y %H:%M') +
                                        ' - Dimensione: ' + str(os.path.getsize(dump_name)) + '\n')
            # zip single sub directory
            for subdir in subdir_list:
                make_zip(path + '/' + subdir, filename + '_' + subdir)
        else: 
            make_zip(path, filename)
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
        message.append('Subject: [' + socket.gethostname() + '] Backup delle dirs - Esito: ' + esito)
        message.append('From: ' + mail_from)
        message.append('To: ' + ', '.join(mail_to))
        message.append('Backup delle dirs del server ' + socket.gethostname() + '\n')
        message += detail_messages
        message.append('')
        # send email
        server.sendmail(mail_from, mail_to, '\n'.join(message))
