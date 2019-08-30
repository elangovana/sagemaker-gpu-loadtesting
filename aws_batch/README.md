# Register AWS batch job

## Prerequisites
1. Python 3.5+, https://www.python.org/downloads/release/python-350/ 
2. Install pip, see https://pip.pypa.io/en/stable/installing/ 

## Setup
3. Install dependencies for this project
    ```bash
    pip install -r aws_batch/requirements.txt
    ``` 
4. Make sure you have registered the docker image with ECS as detailed in the main [README.md](../README.md) 


## How to run

1. Register a aws batch job
    ```bash
    export PYTHONPATH=./aws_batch
    
    python aws_batch/register_sample_job.py <AWS_ACCOUNT_ID>.dkr.ecr.<AWS_DEFAULT_REGION>.amazonaws.com/sagemaker-stresstest:latest <sageamakerendpoint>
    
    #For full details
    python aws_batch/register_sample_job.py -h 

    ```
2. To submit multiple jobs of the registered type
    ```bash
    export PYTHONPATH=./aws_batch
    
    python aws_batch/submit_multiple_jobs.py arn:aws:batch:<AWS_DEFAULT_REGION>:<AWS_ACCOUNT_ID>:job-definition/sagemaker-loadtest-rig:1 <jobname> <queuename>  <sageamakerendpoint> --numrigs 2 --runfornminutes 20
    
    #For full details
    python aws_batch/submit_multiple_jobs.py -h 

    ```

2. If you go to the AWS Batch console -- Job definition , you will see the new job called aws_batch_python_sample.

5. You can then trigger a new job through the AWS Batch console. Pass in the name of the s3destination as one of the parameters in the job.
