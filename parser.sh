#!/bin/bash
cat *.dmp.txt > secrets.txt | grep 'NT:' secrets.txt -B 3 | grep -v "LM: NA" | cut -d ":" -f 2,3 | sed -e "s#--##g" | sed '/^$/d' | tr -d '[:blank:]' | sed 's/NT://g' | awk '{ printf "%s", $0; if (NR % 3 == 0) print ""; else printf ":" }' | awk -v OFS=":" -F":" '{print $2, $1, $3}' | sed 's/:/\\/' | sed 's/:/:/' | grep -v "\\\$" | sort -u
