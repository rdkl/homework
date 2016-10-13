from dynamic_scheduler import DynamicScheduler


################################################################################
class EDFscheduler(DynamicScheduler):
    def __init__(self):
        DynamicScheduler.__init__(self)

    # --------------------------------------------------------------------------
    def compute_job_priority(self, job):
        # Less value will be served first.
        return int((job.deadline + job.release) * 10 ** 8) + \
               100 * int(job.task_id) + int(job.release)

    # --------------------------------------------------------------------------
    def compute_task_priorities(self, task_list):
        pass

    # --------------------------------------------------------------------------
################################################################################
