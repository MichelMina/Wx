import schedulers
import datetime
if __name__=='__main__' :
    p_fcfs = [
        (1, 7, 2), (2, 13, 2), (3, 3, 2), (4, 9, 2)
    ]
    schedulers.fcfs(p_fcfs)
    schedulers.reset()
    schedulers.draw_svg(["FCFS",
                         [("Sam", 5, 5),
                          ("Mina", 10, 5),
                          ]])

    p_sjf_non = [
        (1, 2, 2), (2, 5, 1), (3, 1, 4), (4, 5, 2)
    ]
    schedulers.sjf_non_preemptive(p_sjf_non)
    schedulers.reset()
    p_priority_non = [
        (1, 2, 2, 1), (2, 0, 1, 3), (3, 1, 4, 4), (4, 0, 2, 2)
    ]
    schedulers.priority_non_preemptive(p_priority_non)
    schedulers.reset()
    p_sjf_pre = [
        (1, 0, 7), (2, 2, 4), (3, 4, 1), (4, 5, 4)
    ]
    schedulers.sjf_preemptive(p_sjf_pre)