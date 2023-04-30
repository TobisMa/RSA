#!/usr/bin/sh
if ! python3 -c "" 2> /dev/null
then
    python -i rsa.py
else
    python3 -i rsa.py
fi