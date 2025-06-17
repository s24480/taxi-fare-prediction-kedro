from kedro.pipeline import Pipeline, node, pipeline

from .nodes import train_model, upload_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=train_model,
                inputs=["taxi_ds_cleaned", "params:taxi_fare_predictor"],
                outputs="taxi_fare_predictions",
                name="train_taxi_ds_predictor",
            ),
            node(
                func=upload_model,
                inputs=["params:taxi_fare_predictor", "params:taxi_fare_predictor_zip"],
                outputs=None,
                name="upload_taxi_ds_predictor",
            )
        ]
    )
