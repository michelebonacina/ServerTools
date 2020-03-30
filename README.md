# Server Tools
A set of tools for managing and monitoring a server state.

## Server check
Checks server disk space free and sends an email if over quota.

Needed pyhon 3.x or more

### servercheck.py
The tool main program.

`python3 servercheck`

Called without params check disks occupation and send an email only if one of them is over quota.

`python3 servercheck report`

Called with report parameter send and email with the occupation status of each discs configured.

### servercheckcfg.py
The tool configuration file.

#### disk_to_check
The list of the disks to check.

It's a standard array of strings with the disk path.

Windows format sample: C:/

Linux format sample: /mnt/disk

#### disk_used_perc_limit'
The occupation limit in percentage. If the disk occupation is over this limit, an email is sent.

#### mail_server
The mail server name or IP address.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_server_port
The port of the mail server.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_server_user
The username used for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_server_password
The password user for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_from
The email address of the sender.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_to
The email address list pf the destination users.


## DB mySQL Backup
Backup databases from a mySQL RDBMS.

Runs only on a Linux server.

Needed pyhon 3.x or more

### mysqlbackup.py
Backup main program.

`python3 mysqlbackup`

For each database in config file calls a mysqldump and stores the gzipped data into the export directory.

At the end send a report email with backup details.

### mysqlbackupcfg.py
Backup configuration file.

#### db_to_backup
The list of the database to backup.

It's a standard array of objects which one is a database to backup.

Each object contains:
. server: database server name or IP
. port: database server port
. user: database user name
. password: database user password
. db_names: a standard array of string with the name of the single database to backup

#### export_dir'
The directory where the database dump file will be saved

#### mail_server
The mail server name or IP address.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_server_port
The port of the mail server.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_server_user
The username used for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_server_password
The password user for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_from
The email address of the sender.

Now is awailable only authenticated access to ad SSL SMTP mail server.

#### mail_to
The email address list pf the destination users.