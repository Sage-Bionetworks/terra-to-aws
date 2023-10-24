#!/usr/bin/env python3

import boto3
from google.cloud import storage
import io


# load list of gcs bucket objects

olist = []
with open('/home/jupyter/buckets/copy_cram/cram.txt') as objects:
    lines = objects.readlines()

    for line in lines:
        line = line.strip('\n')
        if line.endswith(':') == False and line != '':
            olist.append(line)

# define data transfer function

def copy_gcs_to_s3(gcs_bucket, gcs_blob, s3_bucket, s3_blob, project):
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket,user_project=project)

    blob = bucket.blob(gcs_blob)
    data = io.BytesIO()
    blob.download_to_file(data)
    data.seek(0)

    s3 = boto3.client("s3")
    s3.upload_fileobj(data, s3_bucket, s3_blob)

    print("uploaded gs://" + gcs_bucket + "/" + gcs_blob + " to: s3://" + s3_bucket + "/" + s3_blob)


#Run Data Transfer for RNASeq

for i in olist:
    blob = i.split('gs://amp-pd-genomics/')[1:][0]
    aws = "AMPSBI/Genomics/samples/CRAM_batch1/" + blob.split('/')[-1]
    copy_gcs_to_s3("amp-pd-genomics",blob,"strides-ampad-project-tower-bucket",aws,"")
