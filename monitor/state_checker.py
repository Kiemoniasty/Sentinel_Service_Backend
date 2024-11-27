import threading
import time
import schedule
from databases.init_sentineldb import Settings
from models.service import Service
from monitor.ping import HealthChecker


class StateChecker:
    """StateChecker class to manage scheduled tasks for health checks."""

    def __init__(self):
        self.cease_continuous_run = None

    @staticmethod
    def schedule_task(service: Service):
        """
        Add a new task for a specific service.
        """
        settings = Settings.query.filter_by(guid=service.setting_guid).first()
        if not settings:
            print(f"Settings not found for service: {service.guid}")
            return

        def job():
            HealthChecker.ping_service(
                self=None,
                address=settings.address,
                timeout=settings.response_time,
                count=settings.number_of_samples,
            )

        # Schedule the job with the service GUID as its tag
        schedule.every(settings.frequency).seconds.do(job).tag(service.guid)
        print(f"Task added for service '{service.guid}'.")

    @staticmethod
    def stop_task_by_tag(tag):
        """
        Stop a scheduled job by its tag.
        """
        schedule.clear(tag)
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

        for service in Service.query.all():
            settings = Settings.query.filter_by(guid=service.setting_guid)
            if settings.status == "ACTIVE":
                self.schedule_task(service)

        print("All tasks scheduled.")
