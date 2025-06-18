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
                outputs="taxi_ds_cleaned",
                name="prepare_taxi_ds",
            )
        ]
    )
