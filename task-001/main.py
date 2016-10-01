#!/usr/bin/env python
# encoding: utf-8

str_input = raw_input("pls input stm>")


#method 1
str_out = list(str_input.decode(encoding="utf-8"))
str_out.reverse()
print "".join(str_out)

#method 2
print str_input.decode(encoding="utf-8")[::-1]
