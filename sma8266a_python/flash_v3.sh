#! /usr/bin/env bash
echo Your flash will be emptied...  Type ^c to bail out!
echo Put your board in program mode and type return...
read
echo esptool.py --port $1 erase_flash
esptool.py --port $1 erase_flash
echo Put your board into program mode again and type return...
read
echo esptool.py --port $1 write_flash 0x0 $2
esptool.py --port $1 write_flash 0x0 $2
echo Python is on your board

