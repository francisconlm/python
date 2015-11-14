#!/usr/bin/env python

"""pgrep.queue.py: Implementation of parallel grep using Queue.Queue."""

__author__      = "Francisco Martins"

import argparse
import sys
import os
from multiprocessing import Process, Array, Semaphore, Value
from ctypes import c_char_p
import time

#creates a parser for our arguments
parser = argparse.ArgumentParser(description = "Exemplo.")
parser.add_argument('-p', dest = 'proc',type = int, default = 1)
parser.add_argument(dest = 'word', type = str)
parser.add_argument(nargs = '+', dest = 'fich', type = str)
arguments = parser.parse_args()

processos = []
numberOfFiles = len(arguments.fich)
fila = Array(c_char_p, numberOfFiles)
proximoFila = Value("i",0)
mutex = Semaphore(1)
empty = Semaphore(numberOfFiles) 

searchWord = arguments.word

for i in range(len(arguments.fich)):
    fila[i] = arguments.fich[i]

#fich e searchWord tem de ser strings
def analise():
    #numero de linhas em que aparece a palavra
    while(proximoFila.value < numberOfFiles):
        wordcounter = 0
        mutex.acquire()
        empty.acquire()
        fileName = fila[proximoFila.value]
        proximoFila.value += 1
        mutex.release()
        f = open(fileName, 'r')
        for line in f:
            if searchWord in line:
                wordcounter += 1
        f.close()
        print "Number of occorencies in -",fileName, "- :" , wordcounter , ". Processed by",os.getpid()
        time.sleep(1) #descanso um pouco

for x in range(arguments.proc):
    NewP = Process(target=analise)
    processos.append(NewP)
    NewP.start()

for p in processos:
    p.join()
