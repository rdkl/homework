import copy

from schedulers.edf_scheduler import EDFscheduler


# ------------------------------------------------------------------------------
# Colored output in console (useful for MISSED jobs).
def print_red(string):
    print '\033[0;31m' + string + '\033[0;m'


# ------------------------------------------------------------------------------
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# ------------------------------------------------------------------------------
def lcm(a, b):
    return a * b // gcd(a, b)


# ------------------------------------------------------------------------------
def lcm_args(*args):
    return reduce(lcm, args)


# ------------------------------------------------------------------------------
def compute_utilization(task_set):
    return sum([task.exectime / task.period for task in task_set])


# ------------------------------------------------------------------------------
# Assumed, that task set is schedulable.
def compute_breakdown_utilization(task_set, context_switch_time, is_preemptive):
    multiplier = 1.0
    hyperperiod = lcm_args(*[int(item.period) for item in task_set])
    step = 0.1
    last_utilization = None

    while True:
        test_set = copy.deepcopy(task_set)

        for task in test_set:
            task.exectime *= multiplier

        scheduler = EDFscheduler()
        completed = scheduler.generate_schedule_with_switches(
            hyperperiod, test_set, context_switch_time,
            is_preemptive=is_preemptive)

        schedulable = True
        for item in completed:
            if item.finish - item.release > item.deadline:
                schedulable = False

        print multiplier, "%.4lf" % compute_utilization(test_set)

        if last_utilization is None:
            last_utilization = compute_utilization(test_set)
        if schedulable is False:
            if step < 10**-4:
                break
            else:
                step /= 2
                multiplier -= step
        else:
            last_utilization = compute_utilization(test_set)
            multiplier += step

    print last_utilization
    return last_utilization
# ------------------------------------------------------------------------------
