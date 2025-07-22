import aioboto3
import asyncio
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# Configurable parameters
file_name = "image_capture_2025-04-25_19-00-00.jpg"
region = "us-west-1"
site_intervals = [5, 10, 20, 30, 40, 50]  # Number of sites per interval (can be adjusted)

async def upload_file_to_s3(file_name, site, region):
    bucket_name = f'site{site}-simulatedbucket'.lower()
    timestamp = datetime.now()
    s3_key = f"{timestamp.year}/{timestamp.strftime('%B')}/{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"

    session = aioboto3.Session()
    async with session.client("s3", region_name=region) as s3:
        try:
            with open(file_name, 'rb') as data:
                print(f"Uploading to {bucket_name} as {s3_key}")
                await s3.put_object(Bucket=bucket_name, Key=s3_key, Body=data)
                print(f"Uploaded: {bucket_name}/{s3_key}")
        except ClientError as e:
            print(f"ClientError for {bucket_name}: {e}")
        except Exception as e:
            print(f"Error uploading to {bucket_name}: {e}")

def get_seconds_until_next_half_hour():
    now = datetime.now()
    next_half = now.replace(second=0, microsecond=0)
    if now.minute < 30:
        next_half = next_half.replace(minute=30)
    else:
        next_half = (next_half + timedelta(hours=1)).replace(minute=0)
    return (next_half - now).total_seconds()

async def simulate_scheduled_uploads():
    while True:
        wait_time = get_seconds_until_next_half_hour()
        print(f"Waiting {int(wait_time)} seconds until the next scheduled upload...")
        await asyncio.sleep(wait_time)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for site_count in site_intervals:
            print(f"\n{current_time} → Uploading to {site_count} sites...")
            tasks = [upload_file_to_s3(file_name, site, region) for site in range(1, site_count + 1)]
            await asyncio.gather(*tasks)
            print(f"Completed upload to {site_count} sites.\n")

            wait_time = get_seconds_until_next_half_hour()
            print(f"Next batch in {int(wait_time)} seconds...\n")
            await asyncio.sleep(wait_time)

if __name__ == "__main__":
    asyncio.run(simulate_scheduled_uploads())
