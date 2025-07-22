import boto3
import time

# Configuration
region = 'us-west-1'  # Change as needed
prefix = 'site'       # Bucket prefix (e.g., site, camera, location)
suffix = 'simulatedbucket'  # Bucket suffix
start_index = 1
end_index = 300       # Create buckets from site1 to site3000
sleep_between = 0.1    # Seconds to wait between bucket creations (set 0 to disable)

s3 = boto3.client('s3', region_name=region)

for i in range(start_index, end_index + 1):
    bucket_name = f'{prefix}{i}-{suffix}'.lower()

    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        print(f'Created bucket: {bucket_name}')
        if sleep_between > 0:
            time.sleep(sleep_between)

    except s3.exceptions.BucketAlreadyExists:
        print(f'Bucket already exists: {bucket_name}')
    except Exception as e:
        print(f'Error creating bucket {bucket_name}: {e}')
