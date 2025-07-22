#!/bin/bash

TEMPLATE_DIR="templates"
REGION="us-west-1"  # Change this to your AWS region

# Optional: uncomment to build first
# sam build

for template in "$TEMPLATE_DIR"/template_batch*.yaml; do
    stack_name=$(basename "$template" .yaml)

    echo "Deploying $stack_name using $template..."

    # First-time guided deploy to store config, reuse afterward
    if [ ! -f "$TEMPLATE_DIR/${stack_name}_samconfig.toml" ]; then
        sam deploy \
            --template-file "$template" \
            --stack-name "$stack_name" \
            --region "$REGION" \
            --capabilities CAPABILITY_IAM \
            --no-confirm-changeset \
            --config-file "$TEMPLATE_DIR/${stack_name}_samconfig.toml" \
            --guided
    else
        sam deploy \
            --template-file "$template" \
            --stack-name "$stack_name" \
            --region "$REGION" \
            --capabilities CAPABILITY_IAM \
            --no-confirm-changeset \
            --config-file "$TEMPLATE_DIR/${stack_name}_samconfig.toml"
    fi

    echo "$stack_name deployed."
done
