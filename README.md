# dagster_logger_example

This project aims to recreate some unpredictable behaviour of dagster.
Project was generated from `dagster new-project`. Dagster version is `0.15.2`.

### Problem setup
Here im trying to do some work in parallel with `concurrent.futures.ThreadPoolExecutor` then when one piece of work done -> yield asset for some sensor.
The problem is in using a dagster `context.log` invocation inside `concurrent.futures.Future` - it's preventing asset materialisation.

In `minimal_example/ops/hello` there is `hello` op that recreates a problem. There is 2 parts:
 - try to execute `work` function for 3 times supplying `context.log` to it, but not using `log`. 
 - try to do the same with `work_logger` function that will log messages by calling `logger.info`

on every future Im waiting for result and when it's ready - yielding some asset materialisation.
For the first step all ok - there will be 3 assets events. But for second step - only one asset at the end.

### Evidences
This happens when running on `dagit` or with command line `dagster job execute -f minimal_example/jobs/say_hello.py`. 
However, when testing events by pytests - there are 6 `ASSET_MATERIALIZATION` events in event stream
(running test: `pytest minimal_example_tests/test_grap
hs/test_say_hello.py -vv`)

### Instruction to recreate
```bash
git clone https://github.com/oyvsyo/dagster_logger_example.git
cd dagster_logger_example/
python3.7 -m venv env
source env/bin/activate
pip install .
dagster job execute -f minimal_example/jobs/say_hello.py
```
