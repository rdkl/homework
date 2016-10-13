import random

import Job

################################################################################
class Task(object):
    id_counter = 0

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
            # task_id = random.randint(10, 99)
            task_id = Task.id_counter
            Task.id_counter += 1
        else:
            Task.id_counter = max(Task.id_counter, task_id + 1)
        if task_id == 34:
            pass

        self.task_id = task_id
        self.jobs_list = []

    # --------------------------------------------------------------------------
    def generate_jobs_list(self, release_bound):
        time = self.phase
        job_id = 0

        while time < release_bound:
            self.jobs_list.append(Job.Job(time,
                                          self.exectime,
                                          self.deadline,
                                          self.task_id,
                                          job_id))
            time += self.period
            job_id += 1

        return self.jobs_list

    # --------------------------------------------------------------------------
    def get_responses(self):
        return [job.compute_response() for job in self.jobs_list]

    # --------------------------------------------------------------------------
    def get_utilization(self):
        return float(self.exectime) / self.period

    # --------------------------------------------------------------------------
    def __str__(self):
        return "Task %d, T: %.1lf, D: %.1lf, C: %.1lf, ph: %.1lf" % (
            self.task_id,
            self.period,
            self.deadline,
            self.exectime,
            self.phase
        )

    # --------------------------------------------------------------------------
################################################################################

if __name__ == "__main__":
    jobs = Task(phase=0.12,
                exectime=1,
                period=2,
                relative_deadline=1.5).generate_jobs_list(12)
    for item in jobs:
        print item