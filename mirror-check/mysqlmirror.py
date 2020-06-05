import os
import smtplib, ssl
import socket
import MySQLdb 
import time
from datetime import date, datetime

from mysqlmirrorcfg import config

# get configuration parameters
master_db_cfg = config['db_master']
slave_db_cfg = config['db_slave']
mail = config['mail']

# prepare result message
detail_messages = []
esito = ''

# connect to master db
master_db = MySQLdb.connect(master_db_cfg['server'], master_db_cfg['user'], master_db_cfg['password'])
# get master info
master_cursor = master_db.cursor()
master_cursor.execute('SHOW MASTER STATUS')
master_data = master_cursor.fetchone()
master_file = master_data[0]
master_position = master_data[1]
# connect to slave db
slave_db = MySQLdb.connect(slave_db_cfg['server'], slave_db_cfg['user'], slave_db_cfg['password'])
# get slave info
slave_cursor = slave_db.cursor()
slave_cursor.execute('SHOW SLAVE STATUS')
slave_data = slave_cursor.fetchone()
slave_file = slave_data[5]
slave_position = slave_data[6]
slave_exec_position = slave_data[21]
# compare log files
recheck = False
# check connection
if master_position != slave_position:
    # connection probably down
    detail_messages.append("Contatore del master sullo slave non allineato. Probabile caduta della connessione.")
# check mirroring
if master_file != slave_file or master_position != slave_exec_position:
    # slave not aligned
    # wait for a while
    time.sleep(10)
    # get slave info
    slave_cursor.execute('SHOW SLAVE STATUS')
    slave_data = slave_cursor.fetchone()
    slave_exec_position_2 = slave_data[21]
    # check slave position
    if slave_exec_position == slave_exec_position_2:
        # position unchanged
        detail_messages.append("Contatore di esecuzione dello slave fermo. Probabile blocco della replica.")
# send email ####
if len(detail_messages) > 0:
    # initialize ssl context
    context = ssl.create_default_context()
    # send email
    with smtplib.SMTP_SSL(mail['server'], mail['port'], context=context) as server:
        # log into server
        server.login(mail['user'], mail['password'])
        # prepare mail message
        message = []
        message.append('Subject: [' + socket.gethostname() + '] Errore nella replica del database')
        message.append('From: ' + mail['from'])
        message.append('To: ' + ', '.join(mail['to']))
        message.append('Replica dei database sul server ' + socket.gethostname() + '\n')
        message += detail_messages
        message.append('')
        # send email
        server.sendmail(mail['from'], mail['to'], '\n'.join(message))
