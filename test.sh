#!/usr/bin/env bash

if [ -z "$1" ]; then
    EXECUTABLE="pypy solve.py"
else
    EXECUTABLE=$1
fi

for file in problems/satisfiable/*
do
    if [ "$($EXECUTABLE "$file" | tail -1)" != "SATISFIABLE" ] ; then
        echo "Wrong answer to $file"
        exit 1
    fi
done

for file in problems/unsatisfiable/*
do
    if [ "$($EXECUTABLE "$file" | tail -1)" != "UNSATISFIABLE" ] ; then
        echo "Wrong answer to $file"
        exit 1
    fi
done

echo "OK"
