import boto3
s3_client = boto3.client('s3')
BUCKET_NAME = "aku-bucket-2026"
# 1. enable object versioning
print(f"enabling versioning on {BUCKET_NAME} ...")
s3_client.put_bucket_versioning(
    Bucket=BUCKET_NAME,
    VersioningConfiguration={'Status': 'Enabled'}
)
# 2. configure a lifecycle policy
# this rule moves non-current(old) model versions to glacier storage after 30 days
lifecycle_policy = {
    'Rules': [
        {
            'ID': 'ArchiveOldModelVersions',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'models/'},
            'NoncurrentVersionTransitions': [
                {
                    'NoncurrentDays': 30,
                    'StorageClass': 'GLACIER'
                }
            ]
        }
    ]
}

print("Applying Lifecycle Policy ...")
s3_client.put_bucket_lifecycle_configuration(
    Bucket=BUCKET_NAME,
    LifecycleConfiguration=lifecycle_policy
)
# 3. test versioning: upload a "new" model version to the exact same path
FILE_NAME = "model.bin"
with open(FILE_NAME, "w") as f:
    f.write("version_2.0_updated_weights_matrix") #simulating a retrained model

print(f"uploading updated {FILE_NAME} .....")
s3_client.upload_file(FILE_NAME, BUCKET_NAME, f"models/v1/{FILE_NAME}")
print("upload complete!")