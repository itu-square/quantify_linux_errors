# WARNING 
# This is documentation, which just looks like actual things, you can
# copy and paste into your database. I would recommend, that you think
# before you just paste.
# I might have made errors.
# I might not have tested this in the end.
# I might also have made changes to the database structure later.
# So maybe it is just not up to date.

create table configurations (
    hash char(64), 
    original longtext,
    exit_status integer(1), 
    conf_errs text, 
    linux_version varchar(100), 
    primary key (hash, linux_version));


> show columns from configurations;
+---------------+--------------+------+-----+---------+-------+
| Field         | Type         | Null | Key | Default | Extra |
+---------------+--------------+------+-----+---------+-------+
| hash          | char(64)     | NO   | PRI |         |       |
| original      | longtext     | YES  |     | NULL    |       |
| exit_status   | int(1)       | YES  |     | NULL    |       |
| conf_errs     | text         | YES  |     | NULL    |       |
| linux_version | varchar(100) | NO   | PRI |         |       |
+---------------+--------------+------+-----+---------+-------+



create table bugs (
    hash char(64) primary key, 
    type varchar(50), 
    linux_version varchar(100), 
    config char(64), 
    original longtext,
    subsystem varchar(30));

> show columns from bugs;
+---------------+--------------+------+-----+---------+-------+
| Field         | Type         | Null | Key | Default | Extra |
+---------------+--------------+------+-----+---------+-------+
| hash          | char(64)     | NO   | PRI | NULL    |       |
| type          | varchar(50)  | YES  |     | NULL    |       |
| linux_version | varchar(100) | YES  |     | NULL    |       |
| config        | char(64)     | YES  |     | NULL    |       |
| original      | longtext     | YES  |     | NULL    |       |
| subsystem     | varchar(30)  | YES  |     | NULL    |       |
+---------------+--------------+------+-----+---------+-------+



create table files (id integer(11) primary key auto_increment, path varchar(50), line varchar(15), bug_id varchar(64));


> show columns from files;
+--------+-------------+------+-----+---------+----------------+
| Field  | Type        | Null | Key | Default | Extra          |
+--------+-------------+------+-----+---------+----------------+
| id     | int(11)     | NO   | PRI | NULL    | auto_increment |
| path   | varchar(50) | YES  |     | NULL    |                |
| line   | varchar(15) | YES  |     | NULL    |                |
| bug_id | varchar(64) | YES  |     | NULL    |                |
+--------+-------------+------+-----+---------+----------------+
