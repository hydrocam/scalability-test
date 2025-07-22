# Serverless Scalability Testing for Image Segmentation Pipeline

This repository contains code, logs, and analysis related to the scalability testing of a serverless, event-driven image segmentation pipeline using AWS Lambda and Amazon S3. The goal is to evaluate how the pipeline performs under increasing workloads — simulating up to 300 monitoring sites operating concurrently.

##  Repository Structure

├── deployment/
│   └── build_and_push.sh               # Builds and pushes 300 site-specific Docker images to AWS ECR
|
├── lambda_function_and_trigger_setup/
│   ├── lambda_template.py              # Creates Lambda Template
│   ├── bucket_creation.py              # Script to create S3 buckets and configure triggers
|   ├── trigger_setup.py
│   └── template.yaml                   # Optional SAM/CloudFormation template for deployment
│
├── scalability_analysis/
│   ├── scalability_data.csv            # Raw performance logs
│   ├── data_retrieval.ipynb            # Notebook to parse and clean CloudWatch logs
│   └── data_plotting.ipynb             # Notebook to visualize trends and generate plot


## What This Tests

- Cold start latency and total execution time across 1–300 concurrent Lambda invocations
- Image segmentation reliability under scale using containerized, site-specific models
- Log-based performance metrics extraction using CloudWatch
- Scalability trends, bottlenecks, and throughput analysis

---

## Analysis Highlights

Located in `scalability_analysis/`:

- `scalability_data.csv`: Collected runtime and performance metrics for each site
- `data_retrieval.ipynb`: Scripted extraction of logs from AWS
- `data_plotting.ipynb`: Visualizations of execution time, memory use, concurrency scaling, etc.

---

## 🔧 Prerequisites

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

## 🧪 How to Run the Tests

1. **Build and push Docker images to ECR**  
   ```bash
   cd deployment
   ./build_and_push.sh
