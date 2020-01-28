#!/usr/bin/env Python

import subprocess

outlist = []
domains = "/path/to/domains.lst"
output_file = "/path/to/spfout.lst"
spfdomain = "_spf.google.com"

print('\n--==[ SPF record searcher ]==--\n')

def lookup(item):
    a = subprocess.check_output('dig +noall +answer +noidnout txt ' + item, shell=True)
    return a

def chase(item):
    """
    Chase the mulitple SPF records in records to see if record is present in them.
    """
    global outlist
    subs = []
    subs = item.split('\t')
    for i in subs:
        if i.startswith("include:"):
            spf = lookup(i.split(":")[1])
            if spfdomain in spf:
                outlist.append(i)
    return

with open(domains, 'r') as infile:
    for line in infile:
        answer = lookup(line).split('\n')
        for i in answer:
            if "v=spf1" in i and spfdomain in i:
                outlist.append(i)
            elif "v=spf1" in i and i.count("include:") > 1:
                chase(i)
            else:
                pass

with open(output_file, 'a+') as outfile:
    for i in outlist:
        outfile.write(i.split('.\t')[0])

print('Searching for SPF done. Results can be found in: ' + output_file)
