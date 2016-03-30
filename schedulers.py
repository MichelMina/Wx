import datetime
# import gantt
from time import localtime, mktime
from collections import OrderedDict
import Queue as queue
from googlegantt import GanttChart, GanttCategory


def draw_svg(info):
    """
    :param info: List[name, List[Tuples]]
    :return: Bool: True if successful, False otherwise
    """
    # Create a project
    p1 = gantt.Project(name=info[0])
    time_now = mktime(localtime())

    for task in info[1]:
        t = gantt.Task(name=task[0],
                       start=datetime.datetime.fromtimestamp(time_now + task[1]),
                       duration=task[2])
        p1.add_task(t)

    p1.make_svg_for_tasks(filename='test_p1.svg', today=datetime.datetime.now())


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


proc_table = []
avg_waiting = []
avg_turnaround = []
final_ans = []
gantt_chart = OrderedDict()
time = 0


def reset():
    global proc_table, avg_waiting, avg_turnaround, time
    proc_table = []
    avg_waiting = []
    avg_turnaround = []

    time = 0


def fcfs(processes):
    """
    :param processes: list of tuples(ID, arrival time, burst time)
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time

    # ID, Arrival Time, Burst Time, Service Time, Waiting Time, Turnaround Time
    # Turnaround Time = Departure Time - Arrival Time
    # Waiting Time = Service Time - Arrival Time

    # Sort according to arrival time

    # Sort input according to arrival time
    processes.sort(key=lambda tup: tup[1])

    for process in processes:
        proc_table.append(
            [processes.index(process), process[1], process[2], time, (time - process[1]),
             (time + process[2] - process[1])])

        if process[1] > time:
            time = process[1]
        gantt_chart[('P' + str(process[0]))] = time
        avg_waiting.append(time - process[1])
        avg_turnaround.append(time + process[2] - process[1])
        time += process[2]

    # Check for blanks (Idle time)
    """
    TODO
    """

    print (processes)
    print (proc_table)
    print (gantt_chart)
    print ("Average Waiting Time:    " + str(get_avg(avg_waiting)))
    print ("Average Turnaround Time: " + str(get_avg(avg_turnaround)))

    return tuple((get_avg(avg_waiting), get_avg(avg_turnaround)))


def sjf_non_preemptive(processes):
    """
    :param processes: list of tuples(ID, arrival time, burst time)
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time
    print (processes)
    # Waiting Time = Service Time - Arrival Time
    # Sort input according to arrival time and burst time
    processes.sort(key=lambda tup: tup[2])
    processes.sort(key=lambda tup: tup[1])
    print (processes)

    # Add to proc_table
    for process in processes:
        proc_table.append([
            process[0], process[1], process[2]
        ])
        final_ans.append([
            process[0], process[1], process[2]
        ])

    # Calculate total time of execution
    # Total Time = SUM(Burst Time) + Arrival Time of First Process
    total_time = processes[0][1]
    for process in processes:
        total_time += process[2]

    print ("total time: " + str(total_time))
    # Proceed to first process
    time += processes[0][1]
    ready_queue = []

    # Execute first process
    gantt_chart[('P' + str(processes[0][0]))] = processes[0][1]
    proc_table[0].append(processes[0][1])
    time += processes[0][2]
    # Remove from queue
    print (processes[0])
    processes.remove(processes[0])
    while time < total_time:
        # Group all processes where arrival time < current time
        for process in processes:
            if process[1] <= time:
                ready_queue.append(process)

        # Sort ready queue by shortest time
        ready_queue.sort(key=lambda tup: tup[2])
        gantt_chart['P' + str(ready_queue[0][0])] = time
        proc_table[proc_table.index(list(ready_queue[0]))].append(time)
        # Execute shortest job
        time += ready_queue[0][2]
        # Remove from queue
        print (ready_queue[0])
        processes.remove(ready_queue[0])
        ready_queue = []

    # Calculate Average and Turnaround Time
    for process in proc_table:
        avg_waiting.append(process[3] - process[1])
        avg_turnaround.append(process[3] + process[2] - process[1])

    print (proc_table)
    print (avg_waiting)
    print (avg_turnaround)
    print ("AVG Waiting Time:    " + str(get_avg(avg_waiting)))
    print ("AVG Turnaround Time: " + str(get_avg(avg_turnaround)))
    return tuple((get_avg(avg_waiting), get_avg(avg_turnaround)))


def priority_non_preemptive(processes):
    """
    :param processes: list of tuples(ID, arrival time, burst time, priority)
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time
    print (processes)
    # Waiting Time = Service Time - Arrival Time
    # Sort input according to arrival time and priority
    processes.sort(key=lambda tup: tup[3])
    processes.sort(key=lambda tup: tup[1])
    print (processes)

    # Add to proc_table
    for process in processes:
        proc_table.append([
            process[0], process[1], process[2], process[3]
        ])

    # Calculate total time of execution
    # Total Time = SUM(Burst Time) + Arrival Time of First Process
    total_time = processes[0][1]
    for process in processes:
        total_time += process[2]

    print ("total time: " + str(total_time))
    # Proceed to first process
    time += processes[0][1]
    ready_queue = []

    # Execute first process
    gantt_chart[('P' + str(processes[0][0]))] = processes[0][1]
    proc_table[0].append(processes[0][1])
    time += processes[0][2]
    # Remove from queue
    print (processes[0])
    processes.remove(processes[0])
    while time < total_time:
        # Group all processes where arrival time < current time
        for process in processes:
            if process[1] <= time:
                ready_queue.append(process)

        # Sort ready queue by priority
        ready_queue.sort(key=lambda tup: tup[3])
        gantt_chart['P' + str(ready_queue[0][0])] = time
        proc_table[proc_table.index(list(ready_queue[0]))].append(time)
        # Execute shortest job
        time += ready_queue[0][2]
        # Remove from queue
        print (ready_queue[0])
        processes.remove(ready_queue[0])
        ready_queue = []

    # Calculate Average and Turnaround Time
    for process in proc_table:
        avg_waiting.append(process[4] - process[1])
        avg_turnaround.append(process[4] + process[2] - process[1])

    print (gantt_chart)
    print (proc_table)
    print (avg_waiting)
    print (avg_turnaround)
    print ("AVG Waiting Time:    " + str(get_avg(avg_waiting)))
    print ("AVG Turnaround Time: " + str(get_avg(avg_turnaround)))
    return tuple((get_avg(avg_waiting), get_avg(avg_turnaround)))


def round_robin_non_preemptive(processes, time_slice,w,h):
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
    Bub=0
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

    gc = GanttChart('Test Chart', width=800, height=275, progress=(2011, 02, 27))
    on_time = GanttCategory('On Time', '0c0')
    late = GanttCategory('Late', 'ffffff')

    t1 = gc.add_task('Late Task', (2016, 1, 1), duration=0, category=late)

    while Standing_index < len(processes) or Ex_Queue._qsize():

        # if the arrival time of process <= time .. put it into ready
        if Standing_index <= len(processes) - 1:
            dummy = proc_table[Standing_index]
            if dummy[Arrival] <= time:
                Ex_Queue._put(dummy)
                Standing_index += 1

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
                    Bub=0
                t1 = gc.add_task('P' + str(dummy[ID]), depends_on=t1, duration=time_slice, category=on_time)
                time += time_slice
                print("executing P%d at time %d" % (dummy[ID], time - time_slice))
            elif 0 < dummy[Burst] <= time_slice:
                # Update total waiting time
                Total_waiting += (dummy[3] + (time - (dummy[4])))
                # finish the job incrementing the time
                time += dummy[Burst]
                print("ending P%d at time %d" % (dummy[ID], time - dummy[Burst]))
                if Bub:
                    t1 = gc.add_task('Bubble', depends_on=t1, duration=Bub, category=late)
                    Bub=0
                t1 = gc.add_task('P' + str(dummy[ID]), depends_on=t1, duration=dummy[Burst], category=on_time)
        else:
            print("bubble at time = %d" % time)
            Bub+=1
            time += 1
    image = gc.get_image('out.png')
    print ("Average waiting time = %f" % (Total_waiting / len(processes)))
    print image
