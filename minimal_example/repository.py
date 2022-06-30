from dagster import repository

from minimal_example.jobs.say_hello import say_hello_job
from minimal_example.schedules.my_hourly_schedule import my_hourly_schedule
from minimal_example.sensors.my_sensor import my_sensor


@repository
def minimal_example():
    """
    The repository definition for this minimal_example Dagster repository.

    For hints on building your Dagster repository, see our documentation overview on Repositories:
    https://docs.dagster.io/overview/repositories-workspaces/repositories
    """
    jobs = [say_hello_job]
    schedules = [my_hourly_schedule]
    sensors = [my_sensor]

    return jobs + schedules + sensors
