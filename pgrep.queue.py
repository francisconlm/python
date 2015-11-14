#!/usr/bin/env python

"""pgrep.queue.py: Implementation of parallel grep using Queue.Queue."""

__author__      = "Francisco Martins"

import argparse
import sys
import os
from multiprocessing import Process, Queue

#creates a parser for our arguments
parser = argparse.ArgumentParser(description = "Exemplo.")
parser.add_argument('-p', dest = 'proc',type = int, default = 1)
parser.add_argument(dest = 'word', type = str)
parser.add_argument(nargs = '+', dest = 'fich', type = str)
arguments = parser.parse_args()

#fich e searchWord tem de ser strings
def analise(queue, searchWord):
    #numero de linhas em que aparece a palavra
    wordcounter = 0
    while not queue.empty():
        fileName = queue.get()
        f = open(fileName, 'r')
        for line in f:
            if searchWord in line:
                wordcounter += 1
        f.close()
        print "Number of occorencies in -",fileName, "- :" , wordcounter , ". Processed by",os.getpid()

processos = []

fila = Queue()
for f in arguments.fich:
    fila.put(f)

for x in range(arguments.proc):
    NewP = Process(target=analise, args = (fila, arguments.word,))
    processos.append(NewP)
    NewP.start()

for p in processos:
    p.join()
