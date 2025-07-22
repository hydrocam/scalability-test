# Serverless Scalability Testing for Image Segmentation Pipeline

This repository contains code, logs, and analysis related to the scalability testing of a serverless, event-driven image segmentation pipeline using AWS Lambda and Amazon S3. The goal is to evaluate how the pipeline performs under increasing workloads — simulating up to 300 monitoring sites operating concurrently.

## Repository Structure

```bash
Scalability-test:
├───Container Build and Deploy                  # Code and scripts for building container images for Lambda
│   │   .gitignore                              # Ignore files like checkpoints and Python cache
│   │   build_and_push_images.sh               # Bash script to build & push 300 Docker images to AWS ECR
│   │   Dockerfile                              # Docker config for Lambda image packaging
│   │   requirements.txt                        # Python dependencies for the container
│   │   __init__.py                             # Marks folder as a package (for local imports)
│   │
│   ├───Model                                   
│   │       model_checkpoint.pth               # Deep learning model weights used for segmentation
│   │       random_forest_model.pkl            # Pickled regression model for estimating stage height
│   │
│   └───src                                     # Source code used in the containerized Lambda function
│           config.py                          # Configuration values (paths, constants, etc.)
│           config.py.bak                      # Backup of the original config.py
│           database_utils.py                  # Utilities to write results to the PostgreSQL database
│           ground_truth.jpg                   # Ground truth image for IoU verification
│           helpers.py                         # Timestamp extractor, mask operations, etc.
│           image_processor.py                 # Main logic for running segmentation and ROI analysis
│           lambda_handler.py                  # AWS Lambda entry point
│           model_loader.py                    # Loads model weights
│           s3_utils.py                        # Upload/download helper for S3
│           __init__.py                        # Allows import as module
│
├───Lambda Function Creation and Trigger Setup  # Scripts to automate S3 bucket, Lambda, and trigger setup
│       add_trigger.py                         # Adds notification triggers from S3 to Lambda
│       asyncuploadtos3.py                     # Async uploader to simulate camera uploads to S3
│       Bucket_Creation.py                     # Creates 300 site-specific S3 input buckets
│       deploy_all_templates.sh                # Deploys all generated SAM templates using AWS SAM CLI
│       Lambda_Template Creation.py            # Generates SAM templates for Lambda functions (split batches)
│
└───Scalability Analysis                        # Notebooks and logs for analyzing pipeline scalability
        loggroupsretreival.ipynb               # Retrieves log metrics from CloudWatch (latency, errors, etc.)
        logsdata.csv                           # Parsed and structured log output from Lambda invocations
        scalabilityanalysis.ipynb              # Plots and metrics to assess scalability under load

```


## What This Tests

- Cold start latency and total execution time across 1–300 concurrent Lambda invocations
- Image segmentation reliability under scale using containerized, site-specific models
- Log-based performance metrics extraction using CloudWatch
- Scalability trends, bottlenecks, and throughput analysis

## Analysis Highlights

Located in `Scalability Analysis/`:

- `logsdata.csv`: Collected runtime and performance metrics for each site
- `loggroupsretreival.ipynb`: Scripted extraction of logs from AWS
- `scalabilityanalysis.ipynb`: Visualizations of execution time, memory use, concurrency scaling, etc.

## Prerequisites

- AWS CLI with credentials configured
- Docker installed and running
- Python 3.x
- Jupyter installed (e.g., via Anaconda or `pip install notebook`)
- Required Python libraries:
  - `boto3`
  - `matplotlib`
  - `pandas`
  - `seaborn`
  - `numpy`
 
## Funding and Acknowledgments

This research was supported by the Cooperative Institute for Research to Operations in Hydrology (CIROH) with joint funding under award NA22NWS4320003 from the NOAA Cooperative Institute Program and the U.S. Geological Survey. The statements, findings, conclusions, and recommendations are those of the author(s) and do not necessarily reflect the opinions of NOAA or USGS. Utah State University is a founding member of CIROH and receives funding under subaward from the University of Alabama. Additional funding and support have been provided by the Utah Water Research laboratory at Utah State University.

