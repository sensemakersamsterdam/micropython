#! /usr/bin/env bash
./sma8266a_python/flash_v3.sh $1  ./sma8266a_python/latest
echo Transferring files and entering repl
rshell -p $1 rsync workshop /pyboard
rshell -p $1 rsync sma8266a /pyboard
rshell -p $1 repl


