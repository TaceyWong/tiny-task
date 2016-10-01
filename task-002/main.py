#!/usr/bin/env python
# encoding: utf-8

str_input = raw_input("pls input sth >")

str_encode = str_input.decode(encoding="utf-8")
flag = True
for i in  range(len(str_encode)/2):
    if str_encode[i] != str_encode[len(str_encode)-i-1]:
        flag = False

print u"是回文序列" if flag else u"不是回文序列"
