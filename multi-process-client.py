import boto3
import json
import requests
import logging
import sys
import argparse
import time
import os

pid = os.getpid()

parser = argparse.ArgumentParser()
parser.add_argument('--end',type=int , default =1)
args = parser.parse_args()


logging.basicConfig(level=logging.INFO, format='From Client: %(asctime)s - %(process)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

start = 0
end = args.end

url = ''

for j in range(start, end, 1):

    # try:
    #     endpoint_name = 'all-in-one-ai-stable-diffusion-webui-in-2023-06-22-03-46-41-567'
    #     boto3_sm_run_client = boto3.client(
    #         "sagemaker-runtime",
    #         region_name='us-west-2',
    #     )
    #     response_model = boto3_sm_run_client.invoke_endpoint_async(
    #         EndpointName=endpoint_name,
    #         ContentType="application/json",
    #         InputLocation="s3://sagemaker-us-west-2-310850127430/async-endpoint-inputs/all-in-one-ai-stable-diffusion-webui-in-2023-05-29--230529-1307/2023-05-29-13-07-23-368-0b451c14-b6af-4925-bd65-d85fb7bd8607" 
    #     )
    #     output = response_model["OutputLocation"]
    #     print(output)

    json_data = {
    "alwayson_scripts": {
        "task": "text-to-image",
        "sd_model_checkpoint": "135643.safetensors",
        "id_task": "16869",
        "uid": "123",
        "save_dir": "outputs"
    },
    "prompt": "A dog",
    "steps": 20,
    "width": 768,
    "height": 768
}
    
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(json_data)
    response = requests.post(url, data=json_data)



