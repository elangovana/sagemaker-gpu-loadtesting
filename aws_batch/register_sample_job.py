import argparse
import json
import logging
import sys

import boto3

from createrole import create_role
from template_access_policy import create_access_policy
from template_job_definition import get_job_definition

"""
Registers the same job with AWS Batch
"""


class RegisterJob:

    def __init__(self, client=None, account=None, aws_region=None):
        self.client = client or boto3.client('batch')
        self.account = account or boto3.client('sts').get_caller_identity().get('Account')
        self.region = aws_region or boto3.session.Session().region_name

    def run(self, container_name: str, sagemaker_uri: str, job_def_name: str, ncpus: int, memoryInMB):
        """
        Registers a job with aws batch.
        :param s3uri_destination: the name of the s3 bucket that will hold the data
        :param container_name: The name of the container to use e.g 324346001917.dkr.ecr.us-east-2.amazonaws.com/awscomprehend-sentiment-demo:latest
        """
        role_name = "AWSBatchECSRole_{}".format(job_def_name)
        logger = logging.getLogger(__name__)

        # This is mandatory for aws batch
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        access_policy = create_access_policy(sagemaker_uri)

        managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"]

        create_role(role_name, assume_role_policy, access_policy, managed_policy_arns)

        job_definition = get_job_definition(self.account, self.region, container_name, job_def_name, sagemaker_uri,
                                            memoryInMB, ncpus,
                                            role_name)

        logger.info(
            "Creating a job with parameters \n {}".format(json.dumps(job_definition, sort_keys=False, indent=4)))
        reponse = self.client.register_job_definition(**job_definition)
        return reponse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)],
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(__name__)

    parser.add_argument("containerimage",
                        help="Container image, e.g 346001917.dkr.ecr.us-east-2.amazonaws.com/sagemaker-stresstest:latest")

    parser.add_argument("sagemakerendpoint",
                        help="The sagemaker endpoint e.g. https://runtime.sagemaker.us-east-2.amazonaws.com/endpoints/myendoint-20119-08-29-06-26-00-622111/invocations")

    parser.add_argument("--job-name",
                        help="The name of the job", default="sagemaker-loadtest-rig")

    parser.add_argument("--cpus",
                        help="The number of cpus", default=4, type=int)

    parser.add_argument("--memoryMb",
                        help="The memory in MB", default=2000, type=int)

    args = parser.parse_args()

    # Register job
    job = RegisterJob()
    result = job.run(args.containerimage, args.sagemakerendpoint, args.job_name, args.cpus, args.memoryMb)

    logger.info("Completed\n{}".format(json.dumps(result, indent=4)))
