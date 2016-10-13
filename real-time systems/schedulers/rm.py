import dynamic_scheduler


################################################################################
class RMscheduler(dynamic_scheduler.DynamicScheduler):
    def __init__(self):
        dynamic_scheduler.DynamicScheduler.__init__(self)

    # --------------------------------------------------------------------------
    def compute_job_priority(self, job):
        # Less priority is better.
        priority = int(self.priorities[job.task_id] * 10 ** 16) + \
                   int(job.release * 10 ** 8) + int(job.job_id)

        return priority

    # --------------------------------------------------------------------------
    def compute_task_priorities(self, task_list):
        self.priorities = {}
        for task in task_list:
            self.priorities[task.task_id] = task.period

    # --------------------------------------------------------------------------
################################################################################
