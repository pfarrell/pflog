#/usr/bin/env bash

sqlite3 db.sqlite3 "drop table image"
sqlite3 db.sqlite3 "drop table post"
sqlite3 db.sqlite3 "drop table email"
sqlite3 db.sqlite3 "drop table author"
sqlite3 db.sqlite3 "VACUUM"

