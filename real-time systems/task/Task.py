import Job

################################################################################
class Task(object):
    def __init__(self, phase, exectime, period, relative_deadline):
        self.deadline = float(relative_deadline)
        self.phase = float(phase)
        self.exectime = float(exectime)
        self.period = float(period)

        if self.deadline <= self.exectime:
            raise Exception("Incorrect task initialization. "
                            "D: %.2lf C: %.2lf" % (self.deadline,
                                                   self.exectime))

    # --------------------------------------------------------------------------
    def generate_jobs_list(self, release_bound):
        time = self.phase
        jobs_list = []

        while time < release_bound:
            jobs_list.append(Job.Job(time, self.exectime, self.deadline))
            time += self.period

        return jobs_list

    # --------------------------------------------------------------------------
################################################################################

if __name__ == "__main__":
    jobs = Task(0.12, 1, 2, 1.5).generate_jobs_list(12)
    for item in jobs:
        print item