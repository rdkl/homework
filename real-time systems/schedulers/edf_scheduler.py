import dynamic_scheduler


################################################################################
class EDFscheduler(dynamic_scheduler.DynamicScheduler):
    def __init__(self):
        dynamic_scheduler.DynamicScheduler.__init__(self)

    # --------------------------------------------------------------------------
    def compute_job_priority(self, job):
        # Less priority is better.
        return int((job.deadline + job.release) * 10 ** 8) + \
               100 * int(job.task_id) + int(job.release)
        # return int((job.deadline + job.release) * 10 ** 8) + int(job.release)

    # --------------------------------------------------------------------------
    def compute_task_priorities(self, task_list):
        pass

    # --------------------------------------------------------------------------
################################################################################
