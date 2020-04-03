# Server Tools
A set of tools for managing and monitoring a server state.

[Server check](## Server check)

[DB mySQL Backup](## DB mySQL Backup)

[Git Mirror](# Git Mirror)

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

##### export_dir
The directory where the database dump file will be saved

##### filename_prefix
The prefix for the file name, next to the current date. 

##### backup_file_history
The number of days of the backup history. Each time a backup starts, checks for backup files older the this values 
(based on the backup date in the file name) and deletes them.

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

Cloning a git repo from a git provider to another and maintain it synchronized

## Use case

You've got a git repo in github and you want to create and synchronize a clone in gitlab. 

> The replica act as a master/slave system: every modification to the slave will be overritten during sinchronization.

Master repo `git@github.com:johndoe/helloworld.git`

Slave repo  `git@gitlab.com:john.doe/isthesame.git`

> The two repositories can have different names

> In this sample I use ssh connections. you can also use https connection, but with ssh you can run commands without login and password

## How-to

### Setting up the mirroring repo

Update you master repo. 

On your pc create a base folder where cloning the master repo and open a shell in this directory.

Execute:

Clone the master repo for mirroring

`git clone --mirror git@github.com:johndoe/helloworld.git`

Enter into repo dir. The directory structure is different from standard git local repo.

`cd helloworld.git`

Change push repo setting the slave one

`git set-url --push origin git@gitlab.com:john.doe/isthesame.git`

Now this repo is configured for mirroring

### Sync mirrored repo

Update you master repo. 

On your pc enter the base folder where cloned the repo.

Execute:

Enter into repo dir.

`cd helloworld.git`

Download data from master repo

`git fetch -p origin`

Upload data to slave repo

`git push --mirror`

The slave repo is now synchronized with master

## gitmirror.py

Mirroring main program.

`python3 gitmirror.py`

For each repo in config file executes a fetch from master and a push to slave.

> All changes made directly to slave repo will be overwritten

> At the moment the first step (master clone, slave config) have to be done manually

## gitmirrorcfg.py

Mirroring configuration file.

##### git_executable_path

Git executable program path. If git if already in you system PATH environment you can insert here only `git`.

##### repositories

The list of the repositories to synchronize.

Each object contains:
- `name`: the name of the repo, only for visualization purpuse
- `path`: local path where the repo mirror is cloned