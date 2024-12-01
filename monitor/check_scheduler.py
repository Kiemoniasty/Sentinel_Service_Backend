"""Scheduler class to manage scheduled tasks for health checks."""

import threading
import time
import schedule
from enums.sentinel_enums import Status
from monitor.health_checker import HealthChecker


class StateChecker:
    """StateChecker class to manage scheduled tasks for health checks."""

    def __init__(self):
        self.cease_continuous_run = None

    @staticmethod
    def schedule_task(service, settings):
        # def schedule_task(self, service, settings):
        """
        Add a new task for a specific service.
        """

        def job():
            HealthChecker.ping_service(
                guid=service.guid, service=service, settings=settings
            )
            from app.flask import state_checker

            print("Stopping...")
            state_checker.stop()

        def run_threaded(job_func):
            job_thread = threading.Thread(target=job_func)
            job_thread.start()

        # Schedule the job with the service GUID as its tag
        schedule.every(settings.frequency).seconds.do(run_threaded, job).tag(
            str(service.guid)
        )
        print(f"Task added for service '{service.guid}'.")

    @staticmethod
    def stop_task_by_tag(tag):
        # def stop_task_by_tag(self, tag):
        """
        Stop a scheduled job by its tag.
        """
        schedule.clear(str(tag))
        print(f"Task with tag '{tag}' has been stopped.")

    def run_continuously(self, interval=1):
        """
        Run the schedule in the background using a thread.
        """
        self.cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            """Thread class to run the scheduler in the background."""

            def __init__(self, cease_event):
                super().__init__()
                self.cease_event = cease_event

            def run(self):
                while not self.cease_event.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread(self.cease_continuous_run)
        continuous_thread.start()
        print("Background scheduler started.")

    def stop(self):
        """
        Stop the background scheduler.
        """
        if self.cease_continuous_run:
            self.cease_continuous_run.set()
            print("Background scheduler stopped.")

    def schedule_list(self):
        """
        Initialize list of jobs and adding it to the scheduler.
        """
        from models.settings import Settings
        from models.service import Service

        services = Service.query.all()
        for service in services:
            settings = Settings.query.filter_by(guid=service.setting_guid).first()
            if settings.status.name == Status.ACTIVE.name:
                self.schedule_task(service, settings)

        print("All tasks scheduled.")

    def get_task_list(self):
        """
        Get list of all scheduled tasks.
        """

        return schedule.get_jobs()
