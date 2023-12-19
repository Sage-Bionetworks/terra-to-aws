#!/usr/bin/env python3

import boto3
from google.cloud import storage
import io

# define data transfer function
def copy_gcs_to_s3(gcs_bucket, gcs_blob, s3_bucket, s3_blob, project=""):
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket, user_project=project)

    blob = bucket.blob(gcs_blob)
    data = io.BytesIO()
    blob.download_to_file(data,raw_download=True)
    data.seek(0)

    print("Uploaded gs://" + gcs_bucket + "/" + gcs_blob + " to s3://" + s3_bucket + "/" + s3_blob)

    s3 = boto3.client("s3")
    s3.upload_fileobj(data, s3_bucket, s3_blob)

# Load and parse GCP Paths from input file
def main(input_file, s3_prefix, s3_bucket, project=""):
    with open(input_file) as objects:
        for line in objects:
            line = line.strip('\n')
            if not line.endswith(':') and line != '':
                # Split the GCS URL to extract the GCS bucket and object name
                gcs_bucket, gcs_object = line.split('gs://')[1].split('/', 1)

                aws_blob = s3_prefix + "/" + gcs_object
                copy_gcs_to_s3(gcs_bucket, gcs_object, s3_bucket, aws_blob, project)

if __name__ == "__main__":
    # Input Parameters
    input_file = '/home/jupyter/commit/smalltest.txt'
    s3_prefix = "tempcopy"
    s3_bucket = "strides-ampad-project-tower-bucket"
    gcs_project = ""  # Set GCS project here

    main(input_file, s3_prefix, s3_bucket, gcs_project)
