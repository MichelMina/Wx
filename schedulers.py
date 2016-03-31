from collections import OrderedDict
import Queue as queue
from googlegantt import GanttChart, GanttCategory

proc_table = []
avg_waiting = []
avg_turnaround = []
gantt_chart = OrderedDict()
time = 0


def get_avg(values):
    """
    :param values: List containing all values
    :return: Average value of all
    """
    avg = 0.0
    for i in values:
        avg += i

    avg /= len(values)
    return avg


def reset():
    """
    :return: Void
    """
    global proc_table, avg_waiting, avg_turnaround, time
    proc_table = []
    avg_waiting = []
    avg_turnaround = []

    time = 0


def remove_blanks(plist, atime, btime, stime):
    """
    :param plist: List to ammend
    :param atime: arrival time index
    :param btime: burst time index
    :param stime: service time index
    :return: void
    """
    if plist[0][atime] > 0:
        idle_time = plist[0][atime]
        plist.insert(0, [
            -1, 0, idle_time, 0, 0, idle_time
        ])

    for i in range(len(plist)):
        if i == len(plist) - 1:
            break
        idle_time = plist[i + 1][stime] - (plist[i][btime] + plist[i][stime])
        if idle_time > 0:
            # Insert Idle Period
            plist.insert(i + 1, [
                -1, (plist[i][btime] + plist[i][stime]), idle_time,
                (plist[i][btime] + plist[i][stime]), 0, idle_time
            ])


def fcfs(processes):
    """
    :param processes: list of tuples(ID, arrival time, burst time)
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time

    # ID, Arrival Time, Burst Time, Service Time, Waiting Time, Turnaround Time
    # Turnaround Time = Departure Time - Arrival Time
    # Waiting Time = Service Time - Arrival Time

    # Sort input according to arrival time
    processes.sort(key=lambda tup: tup[1])

    gc = GanttChart('Schedule Gantt chart', width=800, height=275, progress=(2011, 02, 27))
    on_time = GanttCategory('Executing', '0c0')
    late = GanttCategory('Bubble', 'ffffff')

    t1 = gc.add_task('Tasks', (2016, 1, 1), duration=processes[0][1], category=late)

    for process in processes:
        if process[1] > time:
            time = process[1]

        proc_table.append(
            [process[0], process[1], process[2], time, (time - process[1]),
             (time + process[2] - process[1])])

        avg_waiting.append(time - process[1])
        avg_turnaround.append(time + process[2] - process[1])
        time += process[2]

    # Check for blanks (Idle time)
    # List, indices of arrival time, burst time, service time

    remove_blanks(proc_table, 1, 2, 3)

    for table in proc_table:
        if table[0] == -1:
            t1 = gc.add_task('Bubble', depends_on=t1, duration=table[2], category=late)
        else:
            t1 = gc.add_task('P%d' % table[0], depends_on=t1, duration=table[2], category=on_time)

    image = gc.get_image('out.png')
    return get_avg(avg_waiting)

def sjf_non_preemptive(processes):
    """
    :param processes: list of tuples(ID, arrival time, burst time)
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time


    # Waiting Time = Service Time - Arrival Time
    # Sort input according to arrival time and burst time
    processes.sort(key=lambda tup: tup[2])
    processes.sort(key=lambda tup: tup[1])


    gc = GanttChart('Schedule Gantt chart', width=800, height=275, progress=(2011, 02, 27))
    on_time = GanttCategory('Executing', '0c0')
    late = GanttCategory('Bubble', 'ffffff')

    t1 = gc.add_task('Tasks', (2016, 1, 1), duration=processes[0][1], category=late)
    # Calculate total time of execution
    # Total Time = SUM(Burst Time) + Arrival Time of First Process
    total_time = processes[0][1]
    for process in processes:
        total_time += process[2]

    print "total time: " + str(total_time)
    # Proceed to first process
    time += processes[0][1]
    ready_queue = []

    # Execute first process
    gantt_chart[('P' + str(processes[0][0]))] = processes[0][1]
    proc_table.append([
        processes[0][0], processes[0][1], processes[0][2], processes[0][1], 0, processes[0][2]
    ])
    time += processes[0][2]
    # Remove from queue
    # print processes[0]
    processes.remove(processes[0])
    while time < total_time:
        # Group all processes where arrival time < current time
        print processes
        for process in processes:
            if process[1] <= time:
                ready_queue.append(process)

        # Sort ready queue by shortest time
        ready_queue.sort(key=lambda tup: tup[2])
        proc_table.append([
            ready_queue[0][0], ready_queue[0][1], ready_queue[0][2], time,
            (time - ready_queue[0][1]), (time + ready_queue[0][2] - ready_queue[0][1])
        ])
        # Execute shortest job
        time += ready_queue[0][2]
        # Remove from queue
        # print ready_queue[0]
        processes.remove(ready_queue[0])
        ready_queue = []

    # Calculate Average and Turnaround Time
    for process in proc_table:
        avg_waiting.append(process[3] - process[1])
        avg_turnaround.append(process[3] + process[2] - process[1])

    # Check for blanks (Idle time)
    remove_blanks(proc_table, 1, 2, 3)

    for table in proc_table:
        if table[0] == -1:
            t1 = gc.add_task('Bubble', depends_on=t1, duration=table[2], category=late)
        else:
            t1 = gc.add_task('P%d' % table[0], depends_on=t1, duration=table[2], category=on_time)

    print proc_table
    # print avg_waiting
    # print avg_turnaround
    print "AVG Waiting Time:    " + str(get_avg(avg_waiting))
    print "AVG Turnaround Time: " + str(get_avg(avg_turnaround))
    return get_avg(avg_waiting)

def priority_non_preemptive(processes):
    """
    :param processes: list of tuples(ID, arrival time, burst time, priority)
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time
    # print processes
    # Waiting Time = Service Time - Arrival Time
    # Sort input according to arrival time and burst time
    processes.sort(key=lambda tup: tup[3])
    processes.sort(key=lambda tup: tup[1])
    # print processes
    gc = GanttChart('Schedule Gantt chart', width=800, height=275, progress=(2011, 02, 27))
    on_time = GanttCategory('Executing', '0c0')
    late = GanttCategory('Bubble', 'ffffff')

    t1 = gc.add_task('Tasks', (2016, 1, 1), duration=processes[0][1], category=late)
    # Calculate total time of execution
    # Total Time = SUM(Burst Time) + Arrival Time of First Process
    total_time = processes[0][1]
    for process in processes:
        total_time += process[2]

    print "total time: " + str(total_time)
    # Proceed to first process
    time += processes[0][1]
    ready_queue = []

    # Execute first process
    proc_table.append([
        processes[0][0], processes[0][1], processes[0][2], processes[0][3], processes[0][1], 0, processes[0][2]
    ])
    time += processes[0][2]
    # Remove from queue
    # print processes[0]
    processes.remove(processes[0])
    while time < total_time:
        # Group all processes where arrival time < current time
        for process in processes:
            if process[1] <= time:
                ready_queue.append(process)

        # Sort ready queue by shortest time
        ready_queue.sort(key=lambda tup: tup[3])
        gantt_chart['P' + str(ready_queue[0][0])] = time
        proc_table.append([
            ready_queue[0][0], ready_queue[0][1], ready_queue[0][2], ready_queue[0][3], time,
            (time - ready_queue[0][1]), (time + ready_queue[0][2] - ready_queue[0][1])
        ])
        # Execute shortest job
        time += ready_queue[0][2]
        # Remove from queue
        # print ready_queue[0]
        processes.remove(ready_queue[0])
        ready_queue = []

    # Calculate Average and Turnaround Time
    for process in proc_table:
        avg_waiting.append(process[4] - process[1])
        avg_turnaround.append(process[4] + process[2] - process[1])

    # Check for blanks (Idle time)
    remove_blanks(proc_table, 1, 2, 4)

    for table in proc_table:
        if table[0] == -1:
            t1 = gc.add_task('Bubble', depends_on=t1, duration=table[2], category=late)
        else:
            t1 = gc.add_task('P%d' % table[0], depends_on=t1, duration=table[2], category=on_time)

    print proc_table
    # print avg_waiting
    # print avg_turnaround
    print "AVG Waiting Time:    " + str(get_avg(avg_waiting))
    print "AVG Turnaround Time: " + str(get_avg(avg_turnaround))
    image = gc.get_image('out.png')
    return get_avg(avg_waiting)

def round_robin_non_preemptive(processes, time_slice):
    """
    :param processes: list of tuples(ID, arrival time, burst time)
    :param time_slice: Time slice used in scheduling : float
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time
    # constants to ease the readability, like #define represents location of each in the tuple of process
    ID = 0
    Arrival = 1
    Burst = 2
    Av_wait = 3
    Last_Arr = 4
    # Index to be used later
    Standing_index = 0
    Total_waiting = 0
    Bub = 0

    # Sort input according to arrival time
    processes.sort(key=lambda tup: tup[1])

    Ex_Queue = queue.Queue(len(processes))

    count = -1
    for process in processes:
        count += 1
        # each process in the table have ID,Arrival time,Burst, its waiting time, its last arrival time
        proc_table.append([process[ID], process[Arrival], process[Burst], 0, process[Arrival]])
        # put whichever arrived at time 0
        if process[Arrival] <= time:
            Ex_Queue.put(proc_table[count])
            Standing_index += 1  # increment standing index (next to be checked if arrived)

    #Creating gantt chart
    gc = GanttChart('Schedule Gantt chart', width=800, height=275, progress=(2011, 02, 27))
    on_time = GanttCategory('Executing', '0c0')
    late = GanttCategory('Bubble', 'ffffff')
    t1 = gc.add_task('Tasks', (2016, 1, 1), duration=0, category=late)

    #Main executing loop
    while Standing_index < len(processes) or Ex_Queue._qsize():

        # if the arrival time of process <= time .. put it into ready
        if Standing_index <= len(processes) - 1:
            dummy = proc_table[Standing_index]
            if dummy[Arrival] <= time:
                Ex_Queue._put(dummy)
                Standing_index += 1

        #if the loop is not empty
        if Ex_Queue._qsize() > 0:

            dummy = Ex_Queue._get()
            if dummy[Burst] > time_slice:
                # executing
                dummy[Burst] = dummy[Burst] - time_slice
                # Increment its total waiting time
                dummy[Av_wait] = dummy[Av_wait] + (time - dummy[Last_Arr])
                # setting its time arrival
                dummy[Last_Arr] = time + time_slice
                # pushing it to the queue
                Ex_Queue.put(dummy)
                if Bub:
                    t1 = gc.add_task('Bubble', depends_on=t1, duration=Bub, category=late)
                    Bub = 0
                t1 = gc.add_task('P' + str(dummy[ID]), depends_on=t1, duration=time_slice, category=on_time)
                time += time_slice

            elif 0 < dummy[Burst] <= time_slice:
                # Update total waiting time
                Total_waiting += (dummy[3] + (time - (dummy[4])))
                # finish the job incrementing the time
                time += dummy[Burst]
                print("ending P%d at time %d" % (dummy[ID], time - dummy[Burst]))
                if Bub:
                    t1 = gc.add_task('Bubble', depends_on=t1, duration=Bub, category=late)
                    Bub = 0
                t1 = gc.add_task('P' + str(dummy[ID]), depends_on=t1, duration=dummy[Burst], category=on_time)
        else:
            Bub += 1
            time += 1
    image = gc.get_image('out.png')
    return (Total_waiting / len(processes))



def sjf_preemptive(processes):
    """
    :param processes: list of tuples(ID, arrival time, burst time)
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time
    # print processes
    # Waiting Time = Service Time - Arrival Time
    # Sort input according to arrival time and burst time
    processes.sort(key=lambda tup: tup[2])
    processes.sort(key=lambda tup: tup[1])
    # print processes
    #Creating gantt chart
    gc = GanttChart('Schedule Gantt chart', width=800, height=275, progress=(2011, 02, 27))
    on_time = GanttCategory('Executing', '0c0')
    late = GanttCategory('Bubble', 'ffffff')
    t1 = gc.add_task('Tasks', (2016, 1, 1), duration=0, category=late)
    # Calculate total time of execution
    # Total Time = SUM(Burst Time) + Arrival Time of First Process
    total_time = processes[0][1]
    for process in processes:
        total_time += process[2]

    print "total time: " + str(total_time)
    # Proceed to first process
    time += processes[0][1]
    ready_queue = []
    old_process = None
    while time < total_time:
        # Group all processes where arrival time < current time
        # ready_queue contains all processes that have already arrived by now
        for process in processes:
            if process[1] <= time:
                ready_queue.append(process)

        # Sort ready queue by shortest time
        ready_queue.sort(key=lambda tup: tup[2])

        PID = ready_queue[0][0]
        ARTIME = ready_queue[0][1]

        BURTIME = 0.1
        SERVTIME = time

        gantt_chart['P' + str(ready_queue[0][0])] = SERVTIME
        if ready_queue[0] is old_process:
            element = proc_table[len(proc_table) - 1]
            proc_table[len(proc_table) - 1] = [
                PID, ARTIME, element[2] + BURTIME, element[3]
            ]
        else:
            proc_table.append([
                PID, ARTIME, BURTIME, SERVTIME
            ])

        # Decrement Burst Time
        temp = (ready_queue[0][0], ready_queue[0][1], ready_queue[0][2] - BURTIME)
        processes[processes.index(ready_queue[0])] = temp
        ready_queue[0] = temp
        if ready_queue[0][2] <= 0:
            processes.remove(ready_queue[0])

        time += BURTIME
        old_process = ready_queue[0]
        ready_queue = []

    print proc_table
    # Calculate Average and Turnaround Time
    ids = []
    served_ids = []
    for i in range(len(proc_table)):
        served_ids.append([proc_table[i][0], i])
        ids.append(proc_table[i][0])

    for i in range(len(proc_table)):
        # one time instance
        waiting_time = 0
        if ids.count(proc_table[i][0]) == 1:
            waiting_time = proc_table[i][3] - proc_table[i][1]
            avg_waiting.append(waiting_time)

        # Multi-instance
        if ids.count(proc_table[i][0]) > 1:
            served_ids.reverse()
            served_ids.sort(key=lambda lst: lst[0])
            for j in range(ids.count(proc_table[i][0])):
                try:
                    dummy = served_ids[j]
                    dummy2 = served_ids[j + 1]
                except IndexError:
                    continue
                if dummy[0] == proc_table[i][0]:
                    if proc_table[served_ids[j][1]][3] - proc_table[served_ids[j + 1][1]][2] > 0:
                        waiting_time += proc_table[served_ids[j][1]][3] - proc_table[served_ids[j + 1][1]][2]
                        served_ids.remove(served_ids[j])
                        served_ids.remove(served_ids[j + 1])
            if waiting_time > 0:
                avg_waiting.append(waiting_time)
                waiting_time = 0

    # print avg_waiting
    # print avg_turnaround
    print "AVG Waiting Time:    " + str(get_avg(avg_waiting))
    for table in proc_table:
        if table[0] == -1:
            t1 = gc.add_task('Bubble', depends_on=t1, duration=table[2], category=late)
        else:
            t1 = gc.add_task('P%d' % table[0], depends_on=t1, duration=table[2], category=on_time)

    image = gc.get_image('out.png')
    return get_avg(avg_waiting)

def priority_preemptive(processes):
    """
    :param processes: list of tuples(ID, arrival time, burst time, priority)
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time
    # print processes
    # Waiting Time = Service Time - Arrival Time
    # Sort input according to arrival time and burst time
    processes.sort(key=lambda tup: tup[3])
    processes.sort(key=lambda tup: tup[1])
    # print processes
    #Creating gantt chart
    gc = GanttChart('Schedule Gantt chart', width=800, height=275, progress=(2011, 02, 27))
    on_time = GanttCategory('Executing', '0c0')
    late = GanttCategory('Bubble', 'ffffff')
    t1 = gc.add_task('Tasks', (2016, 1, 1), duration=0, category=late)
    # Calculate total time of execution
    # Total Time = SUM(Burst Time) + Arrival Time of First Process
    total_time = processes[0][1]
    for process in processes:
        total_time += process[2]

    print "total time: " + str(total_time)
    # Proceed to first process
    time += processes[0][1]
    ready_queue = []
    old_process = None
    while time < total_time:
        # Group all processes where arrival time < current time
        # ready_queue contains all processes that have already arrived by now
        for process in processes:
            if process[1] <= time:
                ready_queue.append(process)

        # Sort ready queue by shortest time
        ready_queue.sort(key=lambda tup: tup[3])

        PID = ready_queue[0][0]
        ARTIME = ready_queue[0][1]

        BURTIME = 0.1
        SERVTIME = time

        gantt_chart['P' + str(ready_queue[0][0])] = SERVTIME
        if ready_queue[0] is old_process:
            element = proc_table[len(proc_table) - 1]
            proc_table[len(proc_table) - 1] = [
                PID, ARTIME, element[2] + BURTIME, element[3], element[4]
            ]
        else:
            proc_table.append([
                PID, ARTIME, BURTIME, ready_queue[0][3], SERVTIME
            ])

        # Decrement Burst Time
        temp = (ready_queue[0][0], ready_queue[0][1], ready_queue[0][2] - BURTIME, ready_queue[0][3])
        processes[processes.index(ready_queue[0])] = temp
        ready_queue[0] = temp
        if ready_queue[0][2] <= 0:
            processes.remove(ready_queue[0])

        time += BURTIME
        old_process = ready_queue[0]
        ready_queue = []

    # Check for blanks (Idle time)
    # remove_blanks(proc_table, 1, 2, 4)

    print proc_table
    # Calculate Average and Turnaround Time
    ids = []
    served_ids = []
    for i in range(len(proc_table)):
        served_ids.append([proc_table[i][0], i])
        ids.append(proc_table[i][0])

    for i in range(len(proc_table)):
        # one time instance
        waiting_time = 0
        if ids.count(proc_table[i][0]) == 1:
            waiting_time = proc_table[i][4] - proc_table[i][1]
            avg_waiting.append(waiting_time)

        # Multi-instance
        if ids.count(proc_table[i][0]) > 1:
            served_ids.reverse()
            served_ids.sort(key=lambda lst: lst[0])
            for j in range(len(served_ids)):
                try:
                    dummy = served_ids[j]
                    dummy2 = served_ids[j+1]
                except IndexError:
                    continue
                if dummy[0] == proc_table[i][0]:
                    if proc_table[served_ids[j][1]][4] - proc_table[served_ids[j + 1][1]][2] > 0:
                        waiting_time += proc_table[served_ids[j][1]][4] - proc_table[served_ids[j + 1][1]][2]
                        served_ids.remove(served_ids[j])
                        served_ids.remove(served_ids[j + 1])
            if waiting_time > 0:
                avg_waiting.append(waiting_time)
                waiting_time = 0

    print "AVG Waiting Time:    " + str(get_avg(avg_waiting))
    for table in proc_table:
        if table[0] == -1:
            t1 = gc.add_task('Bubble', depends_on=t1, duration=table[2], category=late)
        else:
            t1 = gc.add_task('P%d' % table[0], depends_on=t1, duration=table[2], category=on_time)

    image = gc.get_image('out.png')
    return get_avg(avg_waiting)

