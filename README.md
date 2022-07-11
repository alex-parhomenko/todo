# todo
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview
TODO application for PY training - it allows to view/store/update/remove tasks. The tasks can be kept in the storages: local DB __sqlite__ or JSON web-storage __json-server__.
<br><br>
This PY project is based on MVC in OOP.  It contains examples of using: custom exceptions, configparser, logger, REST API(client part) with CRUD-methods, unit-tests.

## Configuration
The application is configurable by __config.ini__ with the next structure by default:
```
[DEFAULT]
; custom | web_storage | db_storage
storage_type = custom

[logger]
name = main
level = INFO
log_file_name = todo.log

[export]
csv_file_name = todo.csv

[web_storage]
url = http://localhost:3000
root_name = todo_list

[db_storage]
db_file_name = todo.db
db_name = tasks
```
where:
- [DEFAULT] - defines type of storage: DB, WEB-storage or a custom choice
- [logger] - a logger configuration
- [export] - a file name of the CSV-export
- [web_storage] - JSON WEB server details: URL, a root name of the storage-data
- [db_storage] - DB cofiguration: DB data-file name and DB table name

## WEB storage
Started by the command: `json-server --watch todo.json`, where the data-file 'todo.json' like `{"todo_list": []}`. The root-object __todo_list__ correcponds to config-value __root_name__.

## Dependencies
* python >=3.5 (sys, pathlib)

## Supported Platforms
* Windows

## Source code
 https://github.com/alex-parhomenko/todo.git

## Contributors
Special thanks to
* [udevgeektutor](https://github.com/udevgeektutor) - Py Tutor

## License
Available under the [MIT License](https://github.com/aesophor/py-todo/blob/master/LICENSE)

