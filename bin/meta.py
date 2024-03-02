#!/usr/bin/python
# -*- coding:utf8 -*
import os
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
parser.add_argument('--level', type=int, choices=[0, 1, 2, 3, 4, 5],
                    action="store", dest="level",
                    help='criticity level, from 0 to 5')

args = parser.parse_args()
print(args.accumulate(args.integers))
print("level = ", args.level)

def print_env(env):
    try:
        print(env, ": ", os.environ[env])
    except Exception as e:
        print ("Unknown environment variable: ", env)
        # print (e)   
    
print ("Command line arguments\n")
print_env('PATH')
print_env('HOME')



print ("bye")