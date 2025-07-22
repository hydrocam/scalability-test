import boto3

region = 'us-west-1'
account_id = '767121720320'  # Replace with your actual AWS account ID
lambda_client = boto3.client('lambda', region_name=region)
s3_client = boto3.client('s3', region_name=region)

for i in range(1, 301):
    site_id = f"site{i}"
    bucket_name = f"{site_id}-simulatedbucket"
    function_name = f"site{i}-lambdafunction"
    lambda_arn = f"arn:aws:lambda:{region}:{account_id}:function:{function_name}"

    try:
        # Step 1: Add permission so S3 can invoke Lambda
        lambda_client.add_permission(
            FunctionName=function_name,
            StatementId=f"{site_id}-trigger",
            Action="lambda:InvokeFunction",
            Principal="s3.amazonaws.com",
            SourceArn=f"arn:aws:s3:::{bucket_name}"
        )
        print(f"✅ Added permission for {function_name}")

    except lambda_client.exceptions.ResourceConflictException:
        print(f"⚠️ Permission already exists for {function_name}")

    # Step 2: Attach bucket notification
    notification_config = {
        'LambdaFunctionConfigurations': [
            {
                'LambdaFunctionArn': lambda_arn,
                'Events': ['s3:ObjectCreated:*']
            }
        ]
    }

    try:
        s3_client.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration=notification_config
        )
        print(f"✅ Trigger set for bucket: {bucket_name} → {function_name}")
    except Exception as e:
        print(f"❌ Error configuring {bucket_name}: {e}")
