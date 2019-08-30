import time
from locust import HttpLocust, TaskSet, task, events
import boto3
import json

import os


class SageMakerEndpointTastSet(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.__config__ = None

    @property
    def data(self):
        return self.config["dataPayload"]

    @property
    def config(self):
        self.__config__ = self.__config__ or self._load_config()
        return self.__config__

    def _load_config(self):
        config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
        with open(config_file, "r") as c:
            return json.loads(c.read())

    @task
    def test_invoke(self):
        # Start run here
        region = self.client.base_url.split("://")[1].split(".")[2]
        endpointname = self.client.base_url.split("/")[-2]

        sagemaker_client = boto3.client('sagemaker-runtime', region_name=region)

        # load image
        img_name = os.path.join(os.path.dirname(__file__), self.data[0])
        with open(img_name, "rb") as f:
            image_bytes = f.read()

        # Invoke sagemaker endpoint via the locust wrapper to track request times
        response = self._locust_wrapper(self._invoke_endpoint, image_bytes, sagemaker_client, endpointname)
        body = response["Body"].read()

    def _invoke_endpoint(self, image_bytes, sagemaker_client, endpointname):
        response = sagemaker_client.invoke_endpoint(
            EndpointName=endpointname,
            Body=image_bytes,
            ContentType='application/binary',
            Accept='application/json'
        )

        return response

    def _locust_wrapper(self, func, *args, **kwargs):
        """
Locust wrapper so that the func fires the sucess and failure events for custom boto3 client
        :param func: The function to invoke
        :param args: args to use
        :param kwargs:
        :return:
        """
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="boto3", name="invoke_endpoint", response_time=total_time,
                                        response_length=0)

            return result
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="boto3", name="invoke_endpoint", response_time=total_time,
                                        exception=e)

            raise e


class SageMakerEndpointLocust(HttpLocust):
    task_set = SageMakerEndpointTastSet
    min_wait = 10
    max_wait = 20
