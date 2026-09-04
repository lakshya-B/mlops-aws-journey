import boto3
s3_client = boto3.client('s3')
BUCKET_NAME = "aku-bucket-2026"
MODEL_KEY = "models/v1/model.bin"
print(f"fetching version history for: {MODEL_KEY}....\n")
# 1. list all versions of the specific model artifact
response = s3_client.list_object_versions(Bucket = BUCKET_NAME, Prefix=MODEL_KEY)
versions = response.get('Versions', [])
# 2. parse and print the history neatly
print(f"{'Version ID': <35} | {'Last Modified': <30} | {'Is Latest?': <10}")
print("-" * 85)
for v in versions:
    version_id = v['VersionId']
    last_modified = str(v['LastModified'])
    is_latest = v['IsLatest']
    print(f"{version_id: <35} | {last_modified: <30} | {str(is_latest): <10}")
# 3. simulate rollback: grab the oldest version ID from your printed list
# the one at the bottom of the printed array is usually the older one
ROLLBACK_VERSION_ID= versions[-1]['VersionId'] #selectes the oldest version
DOWNLOAD_PATH = "rolled_back_model.bin"
print(f"Downloading version [{ROLLBACK_VERSION_ID}] to {DOWNLOAD_PATH}...")
s3_client.download_file(
    Bucket=BUCKET_NAME,
    Key=MODEL_KEY,
    Filename=DOWNLOAD_PATH,
    ExtraArgs={'VersionId': ROLLBACK_VERSION_ID}
)
# 4. verifying the file content matches our first upload data
with open(DOWNLOAD_PATH, "r") as f:
    print(f"\nDownloaded File content: '{f.read()}'")