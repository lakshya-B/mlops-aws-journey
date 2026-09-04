import boto3
import os
# Initialize S3 client
s3_client = boto3.client('s3')
# Defining bucket and file 
BUCKET_NAME = "aku-bucket-2026"
FILE_NAME = "model.bin"
# 1. create a dummy model file locally
with open(FILE_NAME, "w") as f:
    f.write("version_1.0_weights_matrix")
# 2. create the s3 bucket
print(f"Creating bucket: {BUCKET_NAME}...")
s3_client.create_bucket(Bucket=BUCKET_NAME)
# 3. upload the artifact
print(f"uploading {FILE_NAME} to s3 ....")
s3_client.upload_file(FILE_NAME, BUCKET_NAME, f"models/v1/{FILE_NAME}")
print("Upload successful! verify it in your AWS s3 console")