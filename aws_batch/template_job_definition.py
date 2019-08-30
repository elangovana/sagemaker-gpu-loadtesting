def get_job_definition(account, region, container_name, job_def_name, job_param_sagemakerendpoint, memoryInMB, ncpus,
                       role_name):
    """
This is the job definition for this sample job.
    :param account:
    :param region:
    :param container_name:
    :param job_def_name:
    :param memoryInMB:
    :param ncpus:
    :param role_name:
    :return:
    """
    return {
        "jobDefinitionName": job_def_name,
        "type": "container",
        # These are the arguments for the job
        "parameters": {

            "sagemakerendpoint": job_param_sagemakerendpoint,
            "log_level": "INFO",
            "hatchrate": "100",
            "numclients": "1000",
            "runtime": "1h"

        },
        # Specify container & jobs properties include entry point and job args that are referred to in parameters
        "containerProperties": {
            "image": container_name,
            "vcpus": ncpus,
            "memory": memoryInMB,
            "command": [
                "-f",
                "stress.py",
                "--host",
                "Ref::sagemakerendpoint",
                "--no-web",
                "-c",
                "Ref::numclients",
                "-r",
                "Ref::hatchrate",
                "-t",
                "Ref::runtime",

            ],
            "jobRoleArn": "arn:aws:iam::{}:role/{}".format(account, role_name),
            "volumes": [
                {
                    "host": {
                        "sourcePath": "/dev/shm"
                    },
                    "name": job_def_name.replace("-", "")
                }
            ],
            "environment": [
                {
                    "name": "AWS_DEFAULT_REGION",
                    "value": region
                }
            ],
            "mountPoints": [
                {
                    "containerPath": "/data",
                    "readOnly": False,
                    "sourceVolume": job_def_name.replace("-", "")
                }
            ],
            "readonlyRootFilesystem": False,
            "privileged": True,
            "ulimits": [],
            "user": ""
        },
        "retryStrategy": {
            "attempts": 1
        }
    }
