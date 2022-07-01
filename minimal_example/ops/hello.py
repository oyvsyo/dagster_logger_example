import time
import logging
from concurrent.futures import ThreadPoolExecutor
from dagster import op, AssetMaterialization, AssetKey, Nothing, Out


def work(i: int, logger) -> int:
    time.sleep(30)
    return logger


def work_logger(i: int, logger) -> int:
    logger.info(f'working {i}')
    time.sleep(30)
    return logger


@op(out=Out(Nothing))
def hello(context):
    """
    An op definition. This example op outputs a single string.

    For more hints about writing Dagster ops, see our documentation overview on Ops:
    https://docs.dagster.io/concepts/ops-jobs-graphs/ops
    """

    futures = []
    executor = ThreadPoolExecutor(1)
    for i in range(3):
        f = executor.submit(work, i, context.log)
        futures.append(f)

    for f in futures:
        context.log.info(f"waiting future done")
        res = f.result()
        yield AssetMaterialization(
            asset_key=AssetKey('asset'),
            metadata={"logger": str(res)},
        )
        context.log.info(f"future done {res}")

    context.log.warning("Starting jobs with logger in futures")

    futures = []

    logger = logging.getLogger('my_logger')
    for i in range(3):
        f = executor.submit(work_logger, i, logger)
        futures.append(f)

    for f in futures:
        context.log.info(f"waiting future done")
        res = f.result()
        yield AssetMaterialization(
            asset_key=AssetKey('asset'),
            metadata={"logger": str(res)},
        )
        context.log.info(f"future done {res}")

    return Nothing
