import abc
from Queue import PriorityQueue

import basic_scheduler
from utils import fixed_more

################################################################################
class DynamicScheduler(basic_scheduler.BasicScheduler):
    def __init__(self):
        self.queue = PriorityQueue()
        self.priorities = {}

    # --------------------------------------------------------------------------
    @abc.abstractmethod
    def compute_task_priorities(self, task_list):
        pass

    # --------------------------------------------------------------------------
    def generate_schedule(self,
                          time_bound,
                          task_list,
                          context_switch_time_constant,
                          is_preemptive=True,
                          print_debug_info=False):
        is_more = lambda x, y: fixed_more(x, y, 10 ** -6)
        is_equal =  lambda x, y: not is_more(x, y) and not is_more(y, x)

        jobs = []
        completed_jobs = []

        for task in task_list:
            jobs += task.generate_jobs_list(time_bound)

        self.compute_task_priorities(task_list)

        releases = {}
        for job in jobs:
            if job.release in releases:
                releases[job.release].append(job)
            else:
                releases[job.release] = [job]

        # Last release time should be inf.
        release_times = sorted(releases.keys()) + [10 ** 8]
        release_time_index = 0

        prev_job = None

        time = release_times[release_time_index]
        while time < time_bound or not self.queue.empty():
            # Fix before every iteration.
            context_switch_time = context_switch_time_constant

            # Release all jobs, that should be released by time.
            while is_more(time, release_times[release_time_index]) or \
                    is_equal(time, release_times[release_time_index]):
                if print_debug_info:
                    print "Inserting", time

                for job in releases[release_times[release_time_index]]:
                    self.queue.put((self.compute_job_priority(job), job))

                release_time_index += 1

            # Now time < release_time[index]. If queue is empty (all jobs are
            # completed), move to next job release point. Else get a job to do.
            if self.queue.empty() and time < time_bound:
                time = release_times[release_time_index]
                continue
            else:
                priority, job = self.queue.get()

            # Means we should not switch context (actually we make it for zero
            # time).
            if job == prev_job:
                context_switch_time = 0.0

            # If preemptive, do only part of job until new job release. After
            # that, return your job into active queue (with reduced remaining
            # execution time).
            if is_preemptive and is_more(time + job.remaining_exectime,
                                         release_times[release_time_index]):
                # Context switch is non-preemptive job.
                if is_more(time + context_switch_time,
                           release_times[release_time_index]):
                    # Just make a context switch.
                    time += context_switch_time
                else:
                    # We are able to do a part of job.
                    job.add_working_interval(time + context_switch_time,
                                             release_times[release_time_index])
                    time = release_times[release_time_index]

                # In both cases context switch occurs.
                prev_job = job
                self.queue.put((self.compute_job_priority(job), job))
                continue

            # Otherwise, complete whole job. In preemptive case we have enough
            # time before new job releases, what forces us to rechoose the most
            # important task. In non-preemptive just complete job until the end.
            # job.remaining_exectime changes after new interval addition.
            rt = job.remaining_exectime
            job.add_working_interval(time + context_switch_time,
                                     time + context_switch_time + rt)
            time += rt + context_switch_time
            completed_jobs.append(job)
            prev_job = None

            if print_debug_info:
                print time

        return completed_jobs

    # --------------------------------------------------------------------------
################################################################################
