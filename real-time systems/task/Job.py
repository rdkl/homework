

################################################################################
class Job(object):
    def __init__(self, release, exectime, deadline, task_id, job_id,
                 print_response=True):
        self.release = float(release)
        self.exectime = float(exectime)
        self.deadline = float(deadline)
        self.finish = None
        self.task_id = task_id
        self.job_id = job_id
        self.remaining_exectime = float(exectime)
        self.work_intervals = []
        self.print_response = print_response

    # --------------------------------------------------------------------------
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.task_id == other.task_id and self.job_id == other.job_id
        else:
            return False

    # --------------------------------------------------------------------------
    def __ne__(self, other):
        return not self.__eq__(other)

    # --------------------------------------------------------------------------
    def get_response_time(self):
        if self.finish is None:
            raise ArithmeticError("Job: responce time is not set")
        return self.finish - self.release

    # --------------------------------------------------------------------------
    def set_finish_time(self, finish):
        self.finish = float(finish)

    # --------------------------------------------------------------------------
    def add_working_interval(self, start, finish):
        # print self, self.remaining_exectime
        self.work_intervals.append([start, finish])
        if finish - start > self.remaining_exectime + 10**-6 or \
            start < self.release - 10**-6:
            print self
            raise ArithmeticError("Incorrect work interval [%.2lf, %.2lf]" %
                                  (start, finish))
        self.remaining_exectime -= finish - start
        if self.remaining_exectime < 10**-6:
            self.set_finish_time(finish)

    # --------------------------------------------------------------------------
    def compute_response(self):
        if self.finish is None:
            raise Exception("Response computation attempt for non-completed job")
        return self.finish - self.release

    # --------------------------------------------------------------------------
    def __str__(self):
        if self.finish is None:
            return "Task %d, job %2d (r: %.2lf)" % (self.task_id,
                                                          self.job_id,
                                                          self.release)
        else:
            intervals = []
            for item in self.work_intervals:
                if len(intervals) > 0:
                    if abs(item[0] - intervals[-1][1]) < 10 ** -6:
                        intervals[-1][1] = item[1]
                        continue
                intervals.append(item)

            if not self.print_response:
                return "Task %d, job %2d (r: %.2lf, d:%.1lf, f: %.1lf) %s" % \
                       (self.task_id,
                        self.job_id,
                        self.release,
                        self.release + self.deadline,
                        self.finish,
                        "".join("[%.2lf, %.2lf] " % (item[0], item[1])
                                for item in intervals))

            return "Task %d, job %2d (r: %.2lf, d:%.1lf, f: %.1lf, rt: %.1lf) %s" % \
                   (self.task_id,
                    self.job_id,
                    self.release,
                    self.release + self.deadline,
                    self.finish,
                    self.finish - self.release,
                    "".join("[%.2lf, %.2lf] " % (item[0], item[1])
                            for item in intervals))

    # --------------------------------------------------------------------------
################################################################################

