import os
import smtplib
import ssl
import socket
import logging
from zipfile import ZipFile
from email.mime.text import MIMEText
from datetime import date, datetime
from shutil import copyfile, make_archive

from dirbackupcfg import config

# get configuration parameters
dir_to_backup = config['dir_to_backup']
backup_direct = config['backup_direct']
tmp_export_dir = config['tmp_export_dir']
export_dir = config['export_dir']
backup_dir_copy = config['backup_dir_copy']
backup_dir_copy_cmd = config['backup_dir_copy_cmd']
filename_prefix = config['filename_prefix']
backup_file_history = config['backup_file_history']
log_file_history = config['log_file_history']
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
    logging.debug('make_zip start')
    logging.debug('path: ' + path + ' - filename: ' + filename)
    # get global variables
    global backup_dir, backup_dir_copy, backup_dir_copy_cmd 
    global export_dir, filename_prefix
    global weekly_backup, monthly_backup, yearly_backup
    global esito, detail_messages

    # prepare dump name
    error = False
    start_time = datetime.now()
    dump_name = start_time.strftime('%Y%m%d') + '_daily-' + filename_prefix + '_' + filename 
    # zip dir
    make_archive(backup_dir + os.path.sep + dump_name, 'zip', path)
    dump_name = dump_name + '.zip'
    # prepare result message
    end_time = datetime.now()
    message = 'Backup della dir ' + path + ' nel file ' + backup_dir + os.path.sep + dump_name + '.'
    logging.info(message)
    # success
    esito = 'OK'
    detail_messages.append(message + ' OK!')
    # copy dump file to destination dir
    if (backup_dir_copy == True):
        # copy dump file to destination dir
        sys_command = backup_dir_copy_cmd.replace('[dump_file]', backup_dir + os.path.sep + dump_name)
        result = os.system(sys_command)
        message = 'Copia del file ' + dump_name
        if result != 0:
            # error
            error = True
            detail_messages.append(message + ' ERRORE!!!!')
        else:
            # success
            error = False
            detail_messages.append(message + ' OK!')
        # delete temporary file
        if (not error):
            message = "Cancellazione del file temporaneo " + dump_name
            os.remove(backup_dir + os.path.sep + dump_name)
            error = False
            detail_messages.append(message + ' OK!')
    if not error:
        if (weekly_backup == True and current_date.weekday() == 6):
            # copy to weekly file
            copyfile(export_dir + os.path.sep + dump_name, export_dir + os.path.sep + start_time.strftime('%Y%m%d') + '_weekly-' + filename_prefix + '_' + filename + '.zip')
        if (monthly_backup == True and current_date.day == 1):
            # copy to monthly file
            copyfile(export_dir + os.path.sep + dump_name, export_dir + os.path.sep + start_time.strftime('%Y%m%d') + '_monthly-' + filename_prefix + '_' + filename + '.zip')
        if (yearly_backup == True and current_date.day == 1 and current_date.month == 1):
            # copy to yearly file
            copyfile(export_dir + os.path.sep + dump_name, export_dir + os.path.sep + start_time.strftime('%Y%m%d') + '_yearly-' + filename_prefix + '_' + filename + '.zip')
        message = 'Inizio: ' + start_time.strftime('%d-%m-%Y %H:%M') + ' - Fine: ' + end_time.strftime('%d-%m-%Y %H:%M') + ' - Dimensione: ' + str(os.path.getsize(export_dir + os.path.sep + dump_name))
        logging.info(message)
    detail_messages.append(message + '\n')
    logging.debug('make_zip end')
    return error

# prepare result message
detail_messages = []
error = False
esito = ''
try:
    backup_dir = export_dir
    if not backup_direct: 
        if (os.path.exists(tmp_export_dir) and os.path.isdir(tmp_export_dir)):
            # temporary export dir exists
            backup_dir = tmp_export_dir 
            # remove all file from temporary export dir
            for item in os.listdir(tmp_export_dir):
                # check dir content
                item_path = tmp_export_dir + os.path.sep + item
                if (os.path.isfile(item_path)):
                    # is a file, remove it
                    os.remove(item_path)
        else:
            # temprary export dir not fouded
            error = True
            detail_messages.append('La directory temporanea di export ' + tmp_export_dir + ' non esiste.')
    if not error:
        if (os.path.exists(export_dir) and os.path.isdir(export_dir)):
            # initialize logging
            log_name = export_dir + os.path.sep + datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + filename_prefix + '-dirbackup.log'
            logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.INFO)
            logging.info('Inizio backup: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
            # export dir exists
            # remove old file from export dir ####
            logging.info("Cancellazione vecchi files dalla dir di export")
            current_date = date.today()
            for item in os.listdir(export_dir):
                # check dir content
                item_path = export_dir + os.path.sep + item
                if (os.path.isfile(item_path)):
                    # is a file
                    if (item.find(filename_prefix + '-dirbackup.log') != -1):
                        # is a log file
                        file_date = date.fromtimestamp(os.path.getctime(item_path))
                        if ((current_date - file_date).days > log_file_history):
                            # the file is old, remove it
                            os.remove(item_path)
                    if (item.find('_daily-' + filename_prefix + '_') != -1):
                        # is a daily backup file
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
                logging.debug('path: '+ path + ' - filename: ' + filename + ' - split_dir: ' + str(split_dir))
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
                    if (len(filename_list) > 0):
                        # prepare dump name
                        start_time = datetime.now()
                        dump_name = start_time.strftime('%Y%m%d') + '_daily-' + filename_prefix + '_' + filename + '.zip'
                        dump_name = backup_dir + os.path.sep + dump_name
                        # zip files in dir
                        zip_file = ZipFile(dump_name, 'w')
                        for filename_dir in filename_list:
                            zip_file.write(path + os.path.sep + filename_dir, filename_dir);
                        # prepare result message
                        end_time = datetime.now()
                        message = 'Backup della dir ' + path + ' nel file ' + dump_name + '.'
                        logging.info(message)
                        # success
                        esito = 'OK'
                        detail_messages.append(message + ' OK!')
                        if (weekly_backup == True and current_date.weekday() == 6):
                            # copy to weekly file
                            copyfile(dump_name, export_dir + os.path.sep + start_time.strftime('%Y%m%d') + '_weekly-' + filename_prefix + '_' + filename + '.zip')
                        if (monthly_backup == True and current_date.day == 1):
                            # copy to monthly file
                            copyfile(dump_name, export_dir + os.path.sep + start_time.strftime('%Y%m%d') + '_monthly-' + filename_prefix + '_' + filename + '.zip')
                        if (yearly_backup == True and current_date.day == 1 and current_date.month == 1):
                            # copy to yearly file
                            copyfile(dump_name, export_dir + os.path.sep + start_time.strftime('%Y%m%d') + '_yearly-' + filename_prefix + '_' + filename + '.zip')
                        message = 'Inizio: ' + start_time.strftime('%d-%m-%Y %H:%M') + ' - Fine: ' + end_time.strftime('%d-%m-%Y %H:%M') + ' - Dimensione: ' + str(os.path.getsize(dump_name))
                        logging.info(message)
                        detail_messages.append(message + '\n')
                    # zip single sub directory
                    for subdir in subdir_list:
                        error = error or make_zip(path + os.path.sep + subdir, filename + '_' + subdir)
                else: 
                    error = make_zip(path, filename)
            logging.info('Fine backup: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        else:
            # export dir not finded
            esito = 'ERRORE!!!'
            message = 'La directory di export ' + export_dir + ' non esiste.'
            logging.warning(message)
            detail_messages.append(message)
except BaseException as err:
    # export dir not finded
    esito = 'ERRORE!!!'
    message = 'Errore generale nel backup. ' + str(err)
    detail_messages.append(message)

# send email ####
if len(detail_messages) > 0:
    # initialize ssl context
    context = ssl.create_default_context()
    # send email
    with smtplib.SMTP_SSL(mail_server, mail_server_port, context=context) as server:
        # log into server
        server.login(mail_server_user, mail_server_password)
        # prepare mail message
        message = MIMEText('Backup delle dirs del server ' + socket.gethostname() + '\n' + '\n'.join(detail_messages), 'plain', 'utf-8')
        message['Subject'] = '[' + socket.gethostname() + '] Backup delle dirs - Esito: ' + esito
        message['From'] = mail_from
        message['To'] =', '.join(mail_to)
        # send email
        server.send_message(message)
        server.quit()
logging.info('Fine backup: ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
