import abc
from Queue import PriorityQueue

import basic_scheduler


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
    def generate_schedule(self, time_bound, task_list, is_preemptive=True,
                          print_debug_info=False):
        jobs = []
        completed_jobs = []

        for task in task_list:
            jobs += task.generate_jobs_list(time_bound)

        self.compute_task_priorities(task_list)

        if is_preemptive:
            releases = {}
            for job in jobs:
                if job.release in releases:
                    releases[job.release].append(job)
                else:
                    releases[job.release] = [job]

            release_times = sorted(releases.keys()) + [10 ** 8]
            release_time_index = 0

            time = release_times[release_time_index]
            while time < time_bound or not self.queue.empty():
                if time == release_times[release_time_index]:
                    release_time_index += 1

                    if print_debug_info:
                        print "Inserting", time

                    for job in releases[time]:
                        self.queue.put(
                            (self.compute_job_priority(job), job))

                if self.queue.empty() and time < time_bound:
                    time = release_times[release_time_index]
                    continue
                else:
                    priority, job = self.queue.get()

                if time + job.remaining_exectime > \
                        release_times[release_time_index]:
                    # Do only part of job.
                    job.add_working_interval(time,
                                             release_times[
                                                 release_time_index])
                    time = release_times[release_time_index]
                    self.queue.put((self.compute_job_priority(job), job))
                else:
                    # Complete whole job.
                    rt = job.remaining_exectime
                    job.add_working_interval(time, time + rt)
                    time += rt
                    completed_jobs.append(job)

                    if print_debug_info:
                        print time

        else:
            for job in jobs:
                self.queue.put((self.compute_job_priority(job), job))

            time = 0.0
            while not self.queue.empty():
                priority, job = self.queue.get()
                job.add_working_interval(time, time + job.exectime)
                completed_jobs.append(job)

                time = time + job.exectime

        return completed_jobs

    # --------------------------------------------------------------------------
################################################################################
