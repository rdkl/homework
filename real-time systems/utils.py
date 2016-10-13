import copy

# ------------------------------------------------------------------------------
# Colored output in console (useful for MISSED jobs).
def print_red(string):
    print '\033[0;31m' + string + '\033[0;m'


# ------------------------------------------------------------------------------
# Greatest coomon divisor.
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# ------------------------------------------------------------------------------
# Lowest common multiplier.
def lcm(a, b):
    return a * b // gcd(a, b)


# ------------------------------------------------------------------------------
# Lowest common multiplier for multiple args.
def lcm_args(*args):
    return reduce(lcm, args)


# ------------------------------------------------------------------------------
# Utilization of given task set.
def compute_utilization(task_set):
    return sum([task.exectime / task.period for task in task_set])


# ------------------------------------------------------------------------------
def fixed_more(first, second, precision=10**-6):
    if first > second + precision:
        return True


# ------------------------------------------------------------------------------
# Context switch time does not allow to get whole utilizatoin for task set,
# multiplied by w. Only for EDF (preemptive and non-preemptive). Assumed that
# task set is schedulable. Also, deadlines must be equal to periods.
def compute_breakdown_utilization(task_set, context_switch_time, is_preemptive,
                                  precision=10**-4):
    multiplier = 1.0

    # Schedulabily check by creating schedule for hyperperiod.
    hyperperiod = lcm_args(*[int(item.period) for item in task_set])
    
    multiplier_step = 0.1
    last_utilization = None

    while True:
        # Make new test_set with changed exectime and ckeck its shedulability.
        test_set = copy.deepcopy(task_set)

        for task in test_set:
            task.exectime *= multiplier

        scheduler = EDFscheduler()
        completed = scheduler.generate_schedule_with_switches(
            hyperperiod,
            test_set,
            context_switch_time,
            is_preemptive=is_preemptive
        )

        schedulable = True
        for item in completed:
            if item.finish - item.release > item.deadline:
                schedulable = False

        # print multiplier, "%.4lf" % compute_utilization(test_set)

        if last_utilization is None:
            last_utilization = compute_utilization(test_set)
        if schedulable is False:
            if multiplier_step < precision:
                break
            else:
                multiplier_step /= 2
                multiplier -= multiplier_step
        else:
            last_utilization = compute_utilization(test_set)
            multiplier += multiplier_step

    # print last_utilization
    return last_utilization


# ------------------------------------------------------------------------------
