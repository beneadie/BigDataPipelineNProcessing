#!/bin/bash

nums=""

MLhtml="https://en.wikipedia.org/w/index.php?title=Machine_learning&oldid="

while read -r line
do
   nums+=" $line"
done < article-ids.txt

for num in $nums
do
  filename="wikipedia-ml-raw/machine-learning-$num.html"
  touch $filename
  data=$(wget -qO- "$MLhtml$num")
  echo "$data" > $filename
done
