import abc


################################################################################
class BasicScheduler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    # --------------------------------------------------------------------------
    @abc.abstractmethod
    def generate_schedule(self, time_bound, task_list, context_switch_time):
        pass

    # --------------------------------------------------------------------------
################################################################################
