#!/bin/bash

if test -d "$1"; then
  echo "$1 exists!"
else
  echo "$1 does not exist."
fi
