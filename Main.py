""'''
from _tracemalloc import start
from _tracemalloc import start
Travis Austin Pavelka
Created on Nov 13, 2019
Finished on Nov 16, 2019

Requires: numpy, plotly

Non-preemptive executes till completion
Preemptive switches based off time and priority

formatting used for gantt creation
df = [
        dict(Task="proc0", Start="0000-01-01", Finish="0009-01-01"),
        dict(Task="proc1", Start="0003-01-01", Finish="0006-01-01"),
        dict(Task="proc2", Start="0001-01-01", Finish="0002-01-01")
     ]
     
@author: Travis Austin Pavelka
'''

import numpy as np
import plotly.figure_factory as ff

# global vars: should only be one of these during program execution (~static)
numproc = 0
data = {}
tquantum = 0
df = []
ptr_arrival = 0
ptr_now = 0
executeds = []

# for df in creation of gantt
def taskify(pid):
    return "Process " + str(pid)
# used for creating start and finish fields with gantt yyyy[-mm-dd]
def feildify(time):
    append = '-01-01'
    string = str(time) + append
    # fill with zeros for year field
    if len(string) == 7:
        string = '000' + string
    elif len(string) == 8 :
        string = '00' + string
    elif len(string) == 9:
        string = '0' + string
    return string
# turn the date string back into an
# integer and return it
def decouple(datestr):
    numstr = datestr[0:4]
    num = int(numstr)
    return num
# get the priority of a pid
def priority(pid):
    return data[pid][2]
# get the burst time of a pid
def burst(pid):
    return data[pid][1]
# get the arrival time of a pid
def arrival(pid):
    return data[pid][0]
    # Calculate the average wait time by using the data
    # variable to calculate a list of wait times for each
    # process and then taking the average of the list.
    # Returns the average.
def avgWT():
    global numproc
    global np
    global df
    # Use df to extract all data for a pid to a list.
    # The list will be formatted [start, end, start, end, ...]
    # for the wait time to be calculated. Record each
    # wait time in a waits list to average.
    wts = []
    stend = []
    for pid in range(0, numproc):
        for dict in df:
            if dict['Task'] == ('Process '+str(pid)):
                start = decouple(dict['Start'])
                finish = decouple(dict['Finish'])
                stend.append(start)
                stend.append(finish)
        # calculcate WT for this stend
        index = 0
        sum = stend[index] - arrival(pid)
        if len(stend) > 2:
            index += 2
            while index < len(stend):
                sum += stend[index] - stend[index-1]
                index += 2
        wts.append(sum)
        stend = []
        
    print("The average wait time is: ")
    arr = np.array(wts)
    print(np.average(arr))
    return ''
    
    # Calculate the average turnaround time by using the
    # data variable to calculate a list of turnaround
    # times for each process and then taking the average of
    # the list. Returns the average.
def avgTAT():
    tats = []
    stend = []
    for pid in range(0, numproc):
        for dict in df:
            if dict['Task'] == ('Process '+str(pid)):
                start = decouple(dict['Start'])
                finish = decouple(dict['Finish'])
                stend.append(start)
                stend.append(finish)
        tats.append(stend[-1]-arrival(pid))
        stend = []
    print("The average turnaround time is: ")
    arr = np.array(tats)
    print(np.average(arr))
    return ''

def FCFS():
    global numproc
    global data
    global df
    global ptr_arrival
    global ptr_now
    global executeds
    
    # Processes are executed in the order of which
    # they arrive. Processes may enter the ready
    # queue while other processes are executing.
    # If no processes are in the ready
    # queue, execute until the executed processes
    # equals the number of processes, numproc.
    ready = []
    while not len(executeds) == numproc:
        for i in range(0, numproc):
            if arrival(i) == ptr_arrival:
                ready.append(i)
        if len(ready) > 0:
            task = taskify(ready[0])
            start = feildify(ptr_now)
            finish = feildify(ptr_now + burst(ready[0]))
            df.append(dict(Task=task, Start=start, Finish=finish))
            executeds.append(ready[0])
            ptr_now += burst(ready[0])
            while ptr_arrival < ptr_now:
                ptr_arrival += 1
                for i in range(0, numproc):
                    if arrival(i) == ptr_arrival:
                        ready.append(i)
            del ready[0]
        else:
            ptr_arrival += 1
            ptr_now += 1
    
    # create the gantt chart with the df
    fig = ff.create_gantt(df)
    fig.show()
    
    print()
    print(avgWT())
    print(avgTAT())
def SJF():
    global numproc
    global data
    global df
    global ptr_arrival
    global ptr_now
    global executeds
    
    now_procs = []
    while not len(executeds) == numproc:
        # add all now_procs to list
        for i in range(0, numproc):
            if arrival(i) == ptr_arrival:
                now_procs.append(i)
        
        # this might should be a while?
        if len(now_procs) > 0:
            # execute all now_procs in SJF order,
            # but first execute the first proc...
            # and test for new shortest jobs that might have
            # come in while executing a process before
            # executing the next job.
            # execute the first shortest proc and delete it
            shortest = now_procs[0]
            for proc in now_procs:
                # find shortest proc
                if burst(proc) < burst(shortest):
                    shortest = proc
            if not shortest in executeds:
                executeds.append(shortest)
                task = taskify(shortest)
                start = feildify(ptr_now)
                finish = feildify(ptr_now + burst(shortest))
                ptr_now += burst(shortest)
                df.append(dict(Task=task, Start=start, Finish=finish))
                i = now_procs.index(shortest)
                del now_procs[i]
                while ptr_arrival < ptr_now:
                    ptr_arrival += 1
                    for i in range(0, numproc):
                        if arrival(i) == ptr_arrival:
                            now_procs.append(i)
        else:
            ptr_now += 1
            ptr_arrival += 1
            
        
    # create the gantt chart with the df
    fig = ff.create_gantt(df)
    fig.show()
    
    print()
    print(avgWT())
    print(avgTAT())
def SRJF():
    global numproc
    global data
    global df
    global ptr_arrival
    global ptr_now
    global executeds
    
    # EXECUTE all processes in SRJF order:
    # Start with ptr_arrival and ptr_now at zero
    # and determine what processes exist currently.
    # Execute the shortest process first, but after
    # one unit of time, test if new and shorter procs
    # arrived in now_procs. If a shorter process
    # arrives, calculate the new burst time for the
    # current process and switch to the shorter proc.
    #
    # If no processes existed/exist, increment ptr_arrival
    # and ptr_now by one and test and continue until the
    # number of executed processes equal the number
    # of numproc. Note: executed processes are only
    # executed when their burst time == zero in this
    # algorithm.
    now_procs = []
    while not len(executeds) == numproc:
        for i in range(0, numproc):
            if arrival(i) == ptr_arrival:
                now_procs.append(i)
        if len(now_procs) > 0:
            shortest = now_procs[0]
            for proc in now_procs:
                if burst(proc) < burst(shortest):
                    shortest = proc
            task = taskify(shortest)
            start = feildify(ptr_now)
            finish = feildify(ptr_now + 1)
            df.append(dict(Task=task, Start=start, Finish=finish))
            prev = data[shortest][1]
            new = prev - 1
            arriv = data[shortest][0]
            data[shortest] = (arriv, new)
            if data[shortest][1] == 0:
                executeds.append(shortest)
                item = now_procs.index(shortest)
                del now_procs[item]
            ptr_now += 1
            ptr_arrival += 1
        else:
            ptr_now += 1
            ptr_arrival += 1
        
    # create the gantt chart with the df
    fig = ff.create_gantt(df)
    fig.show()
    
    print()
    print(avgWT())
    print(avgTAT())
def RR():
    global numproc
    global data
    global tquantum
    global df
    global ptr_arrival
    global ptr_now
    global executeds
    
    # Execute until executeds equals numprocs.
    # Processes are only finished when their 
    # remaining burst time equals zero. Processes
    # are executed for the length of time tquantum.
    now_procs = []
    select = -1
    while not len(executeds) == numproc:
        for i in range(0, numproc):
            if arrival(i) == ptr_arrival:
                now_procs.append(i)
        if len(now_procs) > 0:
            length = len(now_procs)
            select = (select + 1) % length
            pid = now_procs[select]
            task = taskify(pid)
            start = feildify(ptr_now)
            if burst(pid) <= tquantum:
                finish = feildify(ptr_now + burst(pid))
                ptr_now += burst(pid)
                item = now_procs.index(pid)
                del now_procs[item]
                if length > 1:
                    select = (select - 1) % (length-1)
                else:
                    select = 0
                executeds.append(pid)
            else:
                finish = feildify(ptr_now + tquantum)
                old = data[pid][1]
                new = old - tquantum
                data[pid] = (arrival(pid), new)
                ptr_now += tquantum
                
            df.append(dict(Task=task, Start=start, Finish=finish))
            while ptr_arrival < ptr_now:
                ptr_arrival += 1
                for i in range(0, numproc):
                    if arrival(i) == ptr_arrival:
                        now_procs.append(i)
            
        else:
            ptr_now += tquantum
            while ptr_arrival < ptr_now:
                ptr_arrival += 1
                for i in range(0, numproc):
                    if arrival(i) == ptr_arrival:
                        now_procs.append(i)
        
    # create the gantt chart with the df
    fig = ff.create_gantt(df)
    fig.show()
    
    print()
    print(avgWT())
    print(avgTAT())
def Pnon():
    global numproc
    global data
    global tquantum
    global df
    global ptr_arrival
    global ptr_now
    global executeds
    
    # A queue is maintained that contains the currently active
    # processes. From this queue the process with the lowest
    # numerical priority is executed. The ptr_arrival time
    # variable is incremented while the number of executed
    # processes is less than the number of processes in the data.
    now_procs = []
    while not len(executeds) == numproc:
        # add all now_procs to list
        for i in range(0, numproc):
            if arrival(i) == ptr_arrival:
                now_procs.append(i)
        
        if len(now_procs) > 0:
            # execute one of the highest priority proc and delete it
            p = now_procs[0]
            for proc in now_procs:
                # find one of the highest priority procs
                if priority(proc) < priority(p):
                    p = proc
            if not p in executeds:
                executeds.append(p)
                task = taskify(p)
                start = feildify(ptr_now)
                finish = feildify(ptr_now + burst(p))
                ptr_now += burst(p)
                df.append(dict(Task=task, Start=start, Finish=finish))
                i = now_procs.index(p)
                del now_procs[i]
                while ptr_arrival < ptr_now:
                    ptr_arrival += 1
                    for i in range(0, numproc):
                        if arrival(i) == ptr_arrival:
                            now_procs.append(i)
        else:
            ptr_now += 1
            ptr_arrival += 1        
        
        
    # create the gantt chart with the df
    fig = ff.create_gantt(df)
    fig.show()
    
    print()
    print(avgWT())
    print(avgTAT())
def Ppre():
    global numproc
    global data
    global df
    global ptr_arrival
    global ptr_now
    global executeds
    
    # Keep processing until the number of executed procs
    # equals the number of total procs. If there are no
    # processes in the ready queue, increment the now time
    # and the arrival time. If there are processes ready,
    # execute a unit of the highest priority, lowest
    # numerical value.
    now_procs = []
    while not len(executeds) == numproc:
        for i in range(0, numproc):
            if arrival(i) == ptr_arrival:
                now_procs.append(i)
        if len(now_procs) > 0:
            p = now_procs[0]
            for proc in now_procs:
                if priority(proc) < priority(p):
                    p = proc
            task = taskify(p)
            start = feildify(ptr_now)
            finish = feildify(ptr_now + 1)
            df.append(dict(Task=task, Start=start, Finish=finish))
            arriv = data[p][0]
            prev = data[p][1]
            new = prev - 1
            prior = data[p][2]
            data[p] = (arriv, new, prior)
            if data[p][1] == 0:
                executeds.append(p)
                item = now_procs.index(p)
                del now_procs[item]
            ptr_now += 1
            ptr_arrival += 1
        else:
            ptr_now += 1
            ptr_arrival += 1
        
        
    # create the gantt chart with the df
    fig = ff.create_gantt(df)
    fig.show()
    
    print()
    print(avgWT())
    print(avgTAT())
    
def getPriorities():
    global numproc
    global data
    
    p = -1
    priorities = []
    for i in range(0, numproc):
        while p < 0:
            p = int(input("What is the priority of proc"+str(i)+
                            "? (1 is highest priority): "))
        priorities.append(p)
        p = -1
    for i in range(0, numproc):
        p = (data[i][0], data[i][1], priorities[i])
        data[i] = p
    print(data)
    print()
def getInput():
    # get input for numproc
    global numproc
    global data
    
    while not numproc > 0:
        numproc = int(input("Enter the number of processes: "))
        
    # seperator output
    print()
    
    # get input for data
    for i in range(0, numproc):
        arrival = int(input("Enter proc"+str(i)+" arrival time: "))
        burst = int(input("Enter proc"+str(i)+" burst time: "))
        group = (arrival, burst)
        data[i] = group
        
    # seperator output
    print()
    
    # allow the user to see if the data is entered correctly
    print("The dataset is: {PID: (Arrival, Burst), ...}\n"+str(data))
    cont = input("Continue? (y/n) ")
        
    # seperator output
    print()
    
    # determine what algorithm to use + specials
    if cont == "y":
        loop = True
        while loop:
            algorithm = input("Is the operation FCFS, SJF, SRJF, RR, Pnon, or Ppre? ")
            if algorithm == "FCFS":
                loop = False
                FCFS()
            elif algorithm == "SJF":
                loop = False
                SJF()
            elif algorithm == "SRJF":
                loop = False
                SRJF()
            elif algorithm == "RR":
                loop = False
                global tquantum
                while not tquantum > 0:
                    tquantum = int(input("What is the time quantum in units? "))
                RR()
            elif algorithm == "Pnon":
                loop = False
                getPriorities()
                Pnon()
            elif algorithm == "Ppre":
                loop = False
                getPriorities()
                Ppre()
            else:
                pass
    else:
        exit(0)

if __name__ == '__main__':
    getInput()
