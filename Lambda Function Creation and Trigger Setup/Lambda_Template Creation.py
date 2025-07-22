import yaml
import os

def generate_two_sam_templates(start, end):
    split = (start + end) // 2

    ranges = [(start, split), (split, end)]
    os.makedirs("templates", exist_ok=True)

    base_function = {
        'Type': 'AWS::Serverless::Function',
        'Properties': {
            'Description': '',
            'MemorySize': 6200,
            'Timeout': 781,
            'Architectures': ['x86_64'],
            'EphemeralStorage': {'Size': 2500},
            'Role': 'arn:aws:iam::<your-account-id>:role/<your-lambda-role>',
            'Environment': {
                'Variables': {
                    'MODEL_BUCKET': '<your-model-bucket>',
                    'CHECKPOINT_KEY': '<your-model-checkpoint>.pth',
                    'DB_HOST': '<your-db-host>',
                    'SEGMENTATIONSIZEL': '1920',
                    'DB_NAME': '<your-db-name>',
                    'DB_USER': '<your-db-user>',
                    'MASKSIZE': '640',
                    'MODEL_TYPE': 'vit_b',
                    'DB_PASSWORD': '<your-db-password>',
                    'SEGMENTATIONSIZEB': '1080',
                }
            },
            'EventInvokeConfig': {
                'MaximumEventAgeInSeconds': 21600,
                'MaximumRetryAttempts': 2,
            },
            'PackageType': 'Image',
            'SnapStart': {'ApplyOn': 'None'},
            'Tags': {'Project': 'your-project-name'},
            'VpcConfig': {
                'SecurityGroupIds': ['<your-security-group-id>'],
                'SubnetIds': ['<your-subnet-id-1>', '<your-subnet-id-2>'],
                'Ipv6AllowedForDualStack': False
            }
        }
    }

    for idx, (batch_start, batch_end) in enumerate(ranges, start=1):
        template = {
            'AWSTemplateFormatVersion': '2010-09-09',
            'Transform': 'AWS::Serverless-2016-10-31',
            'Description': f'SAM Template for Sites {batch_start} to {batch_end - 1}',
            'Resources': {}
        }

        for i in range(batch_start, batch_end):
            logical_id = f"Site{i}LambdaFunction"
            function = yaml.safe_load(yaml.dump(base_function))  # deep copy
            function['Properties']['FunctionName'] = f"site{i}-lambdafunction"
            function['Properties']['ImageUri'] = f'<your-account-id>.dkr.ecr.<your-region>.amazonaws.com/<your-ecr-repo>:site{i}-containerimage'
            function['Properties']['Environment']['Variables']['OUTPUT_BUCKET'] = f"site{i}-segmentedoutput"
            template['Resources'][logical_id] = function

        file_path = f"templates/template_batch{idx}.yaml"
        with open(file_path, "w") as f:
            yaml.dump(template, f, sort_keys=False)
        print(f"Generated {file_path} for sites {batch_start} to {batch_end - 1}")

if __name__ == "__main__":
    generate_two_sam_templates(1, 301)
