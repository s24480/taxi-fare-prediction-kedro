import os
import zipfile

import pandas as pd
from autogluon.common import TabularDataset
from autogluon.tabular import TabularPredictor
from azure.storage.blob import BlobServiceClient
from sklearn.model_selection import train_test_split


def train_model(df: pd.DataFrame, model_save_dir: str):
    train, test = train_test_split(df, test_size=0.2, random_state=42)

    train_data = TabularDataset(train)

    predictor = TabularPredictor(label='fare_amount', path=model_save_dir).fit(train_data=train_data, test_data=test, presets='high_quality')
    predictor.clone_for_deployment(path=model_save_dir + "-deploy", dirs_exist_ok=True)
    predictions = predictor.predict(test)

    return predictions


def _upload_model_to_az(connection_string: str, zip_path: str):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container="asi-model", blob="taxi_fare_predictor.zip")

    with open(zip_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)


def upload_model(taxi_fare_predictor: str, taxi_fare_predictor_zip: str):
    output_dir = os.path.dirname(taxi_fare_predictor_zip)
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(taxi_fare_predictor_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(taxi_fare_predictor + "-deploy"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=taxi_fare_predictor + "-deploy")
                zipf.write(file_path, arcname)

    _upload_model_to_az(os.getenv("BLOB_CONNECTION_STRING"), taxi_fare_predictor_zip)
