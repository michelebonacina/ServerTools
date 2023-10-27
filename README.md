# Server Tools
A set of tools for managing and monitoring a server state.

[Server check](##server-check)

[DB mySQL Backup](##db-mysql-backup)

[Dir Backup](##dir-backup)

[Git Mirror](#git-mirror)

## Server check
Checks server disk space free and sends an email if over quota.

Needed pyhon 3.x or more

### servercheck.py
The tool main program.

`python3 servercheck.py`

Called without params check disks occupation and send an email only if one of them is over quota.

`python3 servercheck.py report`

Called with report parameter send and email with the occupation status of each discs configured.

### servercheckcfg.py
The tool configuration file.

##### disk_to_check
The list of the disks to check.

It's a standard array of strings with the disk path.

Windows format sample: C:/

Linux format sample: /mnt/disk

##### disk_used_perc_limit'
The occupation limit in percentage. If the disk occupation is over this limit, an email is sent.

##### mail_server
The mail server name or IP address.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_port
The port of the mail server.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_user
The username used for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_password
The password user for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_from
The email address of the sender.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_to
The email address list pf the destination users.


## DB mySQL Backup
Backup databases from a mySQL RDBMS.

Runs only on a Linux server.

Needed pyhon 3.x or more

### mysqlbackup.py
Backup main program.

`python3 mysqlbackup.py`

For each database in config file calls a mysqldump and stores the gzipped data into the export directory.

At the end send a report email with backup details.

### mysqlbackupcfg.py
Backup configuration file.

##### db_to_backup
The list of the database to backup.

It's a standard array of objects which one is a database to backup.

Each object contains:
- server: database server name or IP
- port: database server port
- user: database user name
- password: database user password
- db_names: a standard array of string with the name of the single database to backup

##### tmp_export_dir
The temporary directory where the database dump files are saved. All files in this directory are deleted before dumping the database.

##### backup_dir
The final directory where the database dump are copied, if final copy is enabled. The old files are deleted from this directory before dumping the database.

##### backup_dir_copy
If True, the database dump files are copied to destination.

##### backup_dir_copy_cmd
The system command used to copy dump files to destination. This command must contains the pattern `[dump_file]` which is replaced with the file name.

##### filename_prefix
The prefix for the file name, next to the current date. 

##### backup_file_history
The number of days of the backup history. Each time a backup starts, checks for backup files older the this values 
(based on the backup date in the file name) and deletes them.

##### weekly_backup
Activate weekly backup. Every sunday backup is mantained for one week.

##### monthly_backup
Activate monthly backup. Every first day of month backup is mantained till the next month.

##### yearly_backup
Activate yearly backup. Every first day of year backup is mantained till the next year.

##### mail_server
The mail server name or IP address.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_port
The port of the mail server.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_user
The username used for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_password
The password user for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_from
The email address of the sender.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_to
The email address list pf the destination users.


## Dir Backup
Backup dirs into a zip file.

Needed pyhon 3.x or more

### mysqlbackup.py
Backup main program.

`python3 dirbackup.py`

For each dir in config file calls create a zipfile into the export directory.

At the end send a report email with backup details.

### dirbackupcfg.py
Backup configuration file.

##### dir_to_backup
The list of the dirs to backup.

It's a standard array of objects which one is a dir to backup.

Each object contains:
- path: the backup dir full path
- filename: the name of the zipfile to create (other infos will be added)
- split_dir: True - zip path sub dirs as single zip file and main dir with only simple file, False - zip path directly

##### export_dir
The directory where the zipfile will be saved

##### filename_prefix
The prefix for the filename, next to the current date. 

##### backup_file_history
The number of days of the backup history. Each time a backup starts, checks for backup files older the this values 
(based on the backup date in the file name) and deletes them.

##### weekly_backup
Activate weekly backup. Every sunday backup is mantained for one week.

##### monthly_backup
Activate monthly backup. Every first day of month backup is mantained till the next month.

##### yearly_backup
Activate yearly backup. Every first day of year backup is mantained till the next year.

##### mail_server
The mail server name or IP address.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_port
The port of the mail server.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_user
The username used for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_password
The password user for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_from
The email address of the sender.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_to
The email address list pf the destination users.

## Git Mirror

Cloning a git repo from a git provider to another and maintain it synchronized.

## gitmirror.py

Mirroring main program.

`python3 gitmirror.py [--help] [--only-new] [--send-mail]`

- `--help` shows usage infos
- `--only-new` download only new repository, which are not saved on local disk
- `--send-mail` send a report email at the end of the synchronization

For each repo in config file executes a fetch from master and a push to slave.

> All changes made directly to slave repo will be overwritten

> Access to remote repository via ssh using public/private key pair to avoid interactive user password

> This tools requires GitPython lib

## gitmirrorcfg.py

Mirroring configuration file.

##### git_executable_path

Git executable program path. If git if already in you system PATH environment you can insert here only `git`.

##### repositories

The list of the repositories to synchronize.

Each object contains:
- `name`: name of the repo, added to _path_ for full repo pathname
- `path`: local path where the repo mirror is cloned. the repo _name_ is added to this path for full repo pathname
- `source`: source git repo URL, used for cloning repo if not exists locally
- `destination`: destination git repo URL, used for configuring _push_ repo. if setted to 'off' repo is only fetched from source

##### mail_server
The mail server name or IP address.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_port
The port of the mail server.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_user
The username used for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_server_password
The password user for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_from
The email address of the sender.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail_to
The email address list pf the destination users.

## Mirror check
Checks database replica alignment for a mysql db replica.
Connect to db master and slave e check counter for verifying replica alignment. 
If database not aligned, sends an error email.

Needed pyhon 3.x or more

### mysqlmirror.py
The tool main program for mysql replica check.

`python3 mysqlmirror.py`

Connects either to master and slave database and checks replica status.

### mysqlmirrorcfg.py
The tool configuration file.

##### db_master.server
Server name or IP of the mysql master.

##### db_master.port
Port of the mysql master.

##### db_master.user
Username for accessing the mysql master.

##### db_master.password
Password for accessing the mysql master.

##### db_slave.server
Server name or IP of the mysql slave.

##### db_slave.port
Port of the mysql slave.

##### db_slave.user
Username for accessing the mysql slave.

##### db_slave.password
Password for accessing the mysql slave.

##### mail.server
The mail server name or IP address.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail.port
The port of the mail server.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail.user
The username used for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail.password
The password user for mail server authentication.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail.from
The email address of the sender.

Now is awailable only authenticated access to ad SSL SMTP mail server.

##### mail.to
The email address list pf the destination users.
