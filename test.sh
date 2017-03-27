#!/usr/bin/env bash

for file in problems/satisfiable/*
do
    if [ "$(pypy solve.py "$file" | tail -1)" != "SATISFIABLE" ] ; then
        echo "Wrong answer to $file"
        exit 1
    fi
done

for file in problems/unsatisfiable/*
do
    if [ "$(pypy solve.py "$file" | tail -1)" != "UNSATISFIABLE" ] ; then
        echo "Wrong answer to $file"
        exit 1
    fi
done

echo "OK"
