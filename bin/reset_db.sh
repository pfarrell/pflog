#/usr/bin/env bash

sqlite3 db.sqlite3 "drop table image"
sqlite3 db.sqlite3 "drop table document"
sqlite3 db.sqlite3 "drop table video"
sqlite3 db.sqlite3 "drop table post"
sqlite3 db.sqlite3 "drop table email"
sqlite3 db.sqlite3 "drop table author"
sqlite3 db.sqlite3 "VACUUM"

./bin/init.sh --db-only
