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

        releases = {}
        for job in jobs:
            if job.release in releases:
                releases[job.release].append(job)
            else:
                releases[job.release] = [job]

        # Last release time should be inf.
        release_times = sorted(releases.keys()) + [10 ** 8]
        release_time_index = 0

        time = release_times[release_time_index]
        while time < time_bound or not self.queue.empty():
            while time >= release_times[release_time_index]:
                if print_debug_info:
                    print "Inserting", time

                for job in releases[ release_times[release_time_index]]:
                    self.queue.put(
                        (self.compute_job_priority(job), job))

                release_time_index += 1

            # Now time < release_time[index]. If queue is empty (all jobs are
            # completed), move to next job release point.
            if self.queue.empty() and time < time_bound:
                time = release_times[release_time_index]
                continue
            else:
                priority, job = self.queue.get()

            # If preemptive, do only part of job until new job release. After
            # that, return your job into active queue (with reduced remaining
            # execution time).
            if is_preemptive and \
                    time + job.remaining_exectime > \
                    release_times[release_time_index]:
                job.add_working_interval(time,
                                         release_times[
                                             release_time_index])
                time = release_times[release_time_index]
                self.queue.put((self.compute_job_priority(job), job))
                continue

            # Otherwise, complete whole job. In preemptive case we have enough
            # time before new job releases, what forces us to rechoose the most
            # important task. In non-preemptive just complete job until the end.
            # job.remaining_exectime changes after new interval addition.
            rt = job.remaining_exectime
            job.add_working_interval(time, time + rt)
            time += rt
            completed_jobs.append(job)

            if print_debug_info:
                print time

        return completed_jobs

    # --------------------------------------------------------------------------
################################################################################
