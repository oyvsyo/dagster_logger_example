from dagster import RunRequest, SkipReason, asset_sensor, AssetKey

from minimal_example.jobs.say_hello import say_hello_job


@asset_sensor(AssetKey("asset"), job=say_hello_job)
def my_sensor(context, event):
    """
    A sensor definition. This example sensor always requests a run at each sensor tick.

    For more hints on running jobs with sensors in Dagster, see our documentation overview on
    sensors:
    https://docs.dagster.io/overview/schedules-sensors/sensors
    """
    should_run = False
    if should_run:
        yield RunRequest(run_key=None, run_config={})
    else:
        yield SkipReason("Allways skip")
