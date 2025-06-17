from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    prepare_data
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=prepare_data,
                inputs="taxi_ds",
                outputs=[],
                name="prepare_taxi_ds",
            )
        ]
    )
