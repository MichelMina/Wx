import datetime
import gantt
from time import localtime, mktime
from collections import OrderedDict


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
gantt_chart = OrderedDict()
time = 0


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

    # Sort according to arrival time

    # Sort input according to arrival time
    processes.sort(key=lambda tup: tup[1])

    for process in processes:
        if process[1] > time:
            time = process[1]

        proc_table.append(
            [process[0], process[1], process[2], time, (time - process[1]),
             (time + process[2] - process[1])])

        gantt_chart[('P' + str(process[0]))] = time
        avg_waiting.append(time - process[1])
        avg_turnaround.append(time + process[2] - process[1])
        time += process[2]

    # Check for blanks (Idle time)
    # List, indices of arrival time, burst time, service time
    remove_blanks(proc_table, 1, 2, 3)

    print processes
    print proc_table
    print gantt_chart
    print "Average Waiting Time:    " + str(get_avg(avg_waiting))
    print "Average Turnaround Time: " + str(get_avg(avg_turnaround))

    return tuple((get_avg(avg_waiting), get_avg(avg_turnaround)))


def sjf_non_preemptive(processes):
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
        for process in processes:
            if process[1] <= time:
                ready_queue.append(process)

        # Sort ready queue by shortest time
        ready_queue.sort(key=lambda tup: tup[2])
        gantt_chart['P' + str(ready_queue[0][0])] = time
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

    print proc_table
    # print avg_waiting
    # print avg_turnaround
    print "AVG Waiting Time:    " + str(get_avg(avg_waiting))
    print "AVG Turnaround Time: " + str(get_avg(avg_turnaround))
    return tuple((get_avg(avg_waiting), get_avg(avg_turnaround)))


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
        for process in processes:
            if process[1] <= time:
                ready_queue.append(process)

        # Sort ready queue by shortest time
        ready_queue.sort(key=lambda tup: tup[2])
        gantt_chart['P' + str(ready_queue[0][0])] = time
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

    print proc_table
    # print avg_waiting
    # print avg_turnaround
    print "AVG Waiting Time:    " + str(get_avg(avg_waiting))
    print "AVG Turnaround Time: " + str(get_avg(avg_turnaround))
    return tuple((get_avg(avg_waiting), get_avg(avg_turnaround)))


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

    print proc_table
    # print avg_waiting
    # print avg_turnaround
    print "AVG Waiting Time:    " + str(get_avg(avg_waiting))
    print "AVG Turnaround Time: " + str(get_avg(avg_turnaround))
    return tuple((get_avg(avg_waiting), get_avg(avg_turnaround)))


def round_robin_non_preemptive(processes, time_slice):
    """
    :param processes: list of tuples(ID, arrival time, burst time)
    :param time_slice: Time slice used in scheduling : float
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time

    # Sort input according to arrival time
    processes.sort(key=lambda tup: tup[1])
