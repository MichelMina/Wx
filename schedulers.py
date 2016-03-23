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
    print processes
    # Waiting Time = Service Time - Arrival Time
    # Sort input according to arrival time and burst time
    processes.sort(key=lambda tup: tup[2])
    processes.sort(key=lambda tup: tup[1])
    print processes

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

    print "total time: " + str(total_time)
    # Proceed to first process
    time += processes[0][1]
    ready_queue = []

    # Execute first process
    gantt_chart[('P' + str(processes[0][0]))] = processes[0][1]
    proc_table[0].append(processes[0][1])
    time += processes[0][2]
    # Remove from queue
    print processes[0]
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
        print ready_queue[0]
        processes.remove(ready_queue[0])
        ready_queue = []

    # Calculate Average and Turnaround Time
    for process in proc_table:
        avg_waiting.append(process[3] - process[1])
        avg_turnaround.append(process[3] + process[2] - process[1])

    print proc_table
    print avg_waiting
    print avg_turnaround
    print "AVG Waiting Time:    " + str(get_avg(avg_waiting))
    print "AVG Turnaround Time: " + str(get_avg(avg_turnaround))
    return tuple((get_avg(avg_waiting), get_avg(avg_turnaround)))


def priority_non_preemptive(processes):
    """
    :param processes: list of tuples(ID, arrival time, burst time, priority)
    :return: tuple(AVG Waiting time, AVG Turnaround Time)
    """
    global time
    print processes
    # Waiting Time = Service Time - Arrival Time
    # Sort input according to arrival time and priority
    processes.sort(key=lambda tup: tup[3])
    processes.sort(key=lambda tup: tup[1])
    print processes

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

    print "total time: " + str(total_time)
    # Proceed to first process
    time += processes[0][1]
    ready_queue = []

    # Execute first process
    gantt_chart[('P' + str(processes[0][0]))] = processes[0][1]
    proc_table[0].append(processes[0][1])
    time += processes[0][2]
    # Remove from queue
    print processes[0]
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
        print ready_queue[0]
        processes.remove(ready_queue[0])
        ready_queue = []

    # Calculate Average and Turnaround Time
    for process in proc_table:
        avg_waiting.append(process[4] - process[1])
        avg_turnaround.append(process[4] + process[2] - process[1])

    print gantt_chart
    print proc_table
    print avg_waiting
    print avg_turnaround
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
