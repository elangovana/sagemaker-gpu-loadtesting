import argparse
import logging
import sys
from time import sleep

import boto3


def submit_job(job_def, queue_name, sagemaker_endpoint, numclients, hatchrate, runfornminutes):
    client = boto3.client('batch')
    response = client.submit_job(
        jobName='Inference',
        jobQueue=queue_name,
        jobDefinition=job_def,
        parameters={
            "sagemakerendpoint": sagemaker_endpoint,

            "hatchrate": str(hatchrate),
            "numclients": str(numclients),

            "runtime": "{}m".format(str(runfornminutes))

        },
        timeout={
            'attemptDurationSeconds': 86400 * 2
        }
    )

    print(response)


def submit_multiple(job_def, queue_name, sagemaker_endpoint, numclients, hatchrate, runfornminutes, n_rigs=10):
    # Submit job for each prefix
    for _ in range(n_rigs):
        sleep(1)
        submit_job(job_def, queue_name, sagemaker_endpoint, numclients, hatchrate, runfornminutes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)],
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(__name__)

    parser.add_argument("job_name",
                        help="Batch Job def name, e.g sagemaker-stress-tests:11")

    parser.add_argument("queue",
                        help="The name of the job queue", default="sagemaker-stress-tests")

    parser.add_argument("sagemaker_endpoint",
                        help="The sagemaker endpoint e.g. https://runtime.sagemaker.us-east-2.amazonaws.com/endpoints/myendoint-20119-08-29-06-26-00-622111/invocations")

    parser.add_argument("--numrigs",
                        help="The number of clients per rig", type=int, default=2)

    parser.add_argument("--numclients",
                        help="The number of clients per rig", type=int, default=200)

    parser.add_argument("--hatchrate",
                        help="The number of clients hatched at a time", type=int, default=10)

    parser.add_argument("--runfornminutes",
                        help="In minutes", type=int, default=2)

    args = parser.parse_args()

    # Register job
    submit_multiple(args.job_name, args.queue, args.sagemaker_endpoint, args.numclients,
                    args.hatchrate, args.runfornminutes, args.numrigs)

    logger.info("Completed")
