from dagster import DagsterEventType
from minimal_example.jobs.say_hello import say_hello_job


def test_say_hello():
    """
    This is an example test for a Dagster job.

    For hints on how to test your Dagster graphs, see our documentation tutorial on Testing:
    https://docs.dagster.io/concepts/testing
    """
    result = say_hello_job.execute_in_process(
        run_config={
            "execution": {
                "config": {
                    "multiprocess": {
                        "max_concurrent": 1
                    }
                }
            }
        }
    )

    assert result.success
    assert result.output_for_node("hello") is None

    events_for_step = result.events_for_node("hello")
    events = [se.event_type for se in events_for_step]
    assert [se.event_type for se in events_for_step] == [
        DagsterEventType.STEP_START,
        *[DagsterEventType.ASSET_MATERIALIZATION]*6,
        DagsterEventType.STEP_OUTPUT,
        DagsterEventType.HANDLED_OUTPUT,
        DagsterEventType.STEP_SUCCESS,
    ]
