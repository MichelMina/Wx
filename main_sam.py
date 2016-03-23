import schedulers
import datetime
if __name__=='__main__' :
    p_fcfs = [
        (1, 20, 2), (2, 0, 3), (3, 5, 10)
    ]
    schedulers.fcfs(p_fcfs)

    schedulers.draw_svg(["FCFS",
                         [("Sam", 5, 5),
                          ("Mina", 10, 5),
                          ]])

    p_sjf_non = [
        (1, 2, 2), (2, 0, 1), (3, 1, 4), (4, 0, 2)
    ]
    # schedulers.reset()
    # schedulers.sjf_non_preemptive(p_sjf_non)
    # schedulers.reset()
    p_priority_non = [
        (1, 2, 2, 1), (2, 0, 1, 3), (3, 1, 4, 4), (4, 0, 2, 2)
    ]
    # schedulers.priority_non_preemptive(p_priority_non)