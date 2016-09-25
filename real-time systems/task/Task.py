import random

import Job

################################################################################
class Task(object):
    def __init__(self, period, exectime, phase=0.0, relative_deadline=None,
                 task_id=None):
        self.exectime = float(exectime)
        self.period = float(period)
        if relative_deadline is None:
            self.deadline = self.period
        else:
            self.deadline = float(relative_deadline)
        self.phase = float(phase)

        if self.deadline <= self.exectime:
            raise Exception("Incorrect task initialization. "
                            "D: %.2lf C: %.2lf" % (self.deadline,
                                                   self.exectime))

        if task_id is None:
            task_id = random.randint(10, 99)

        self.task_id = task_id

    # --------------------------------------------------------------------------
    def generate_jobs_list(self, release_bound):
        time = self.phase
        jobs_list = []

        job_id = 0

        while time < release_bound:
            jobs_list.append(Job.Job(time,
                                     self.exectime,
                                     self.deadline,
                                     self.task_id,
                                     job_id))
            time += self.period
            job_id += 1

        return jobs_list

    # --------------------------------------------------------------------------
################################################################################

if __name__ == "__main__":
    jobs = Task(phase=0.12,
                exectime=1,
                period=2,
                relative_deadline=1.5).generate_jobs_list(12)
    for item in jobs:
        print item