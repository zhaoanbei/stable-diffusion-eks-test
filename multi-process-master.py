# from multiprocessing import Process
import time
import sys
import logging
import subprocess
import boto3
import traceback
from PIL import Image
from datetime import datetime
import io
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(process)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
args = sys.argv
# print("Command-line arguments:")
# for arg in args:
#     print(arg)
from botocore.exceptions import ClientError

num_of_requests = int(args[1])
interval = int(args[2])
sqsQueueUrl = 'https://sqs.us-east-1.amazonaws.com/544592066775/output'
procs = []
normals = []
abnormals = []
SQS_WAIT_TIME_SECONDS = 1

s3_resource = boto3.resource("s3")
def get_bucket_and_key(s3uri):
    pos = s3uri.find("/", 5)
    bucket = s3uri[5:pos]
    key = s3uri[pos + 1 :]
    return bucket, key

def receive_messages(queue, max_number, wait_time):
    """
    Receive a batch of messages in a single request from an SQS queue.

    :param queue: The queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    try:
        messages = queue.receive_messages(
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time,
            AttributeNames=['All'],
            MessageAttributeNames=['All']
        )
    except Exception as error:
        logger.error(f"Error receiving messages: {error}")
    else:
        return messages

def delete_message(message):
    """
    Delete a message from a queue. Clients must delete messages after they
    are received and processed to remove them from the queue.

    :param message: The message to delete. The message's queue URL is contained in
                    the message's metadata.
    :return: None
    """
    try:
        message.delete()
    except ClientError as error:
        traceback.print_exc()
        raise error

# send request
i = 0
for i in range(num_of_requests):
    logger.info(f"This is request number: {i}")
    # Start the child process
    proc = subprocess.Popen(['python', 'multi-process-client.py'], stdout=subprocess.PIPE)
    procs.append(proc)
    # Do other things while the process is running
    logger.info(f"sleeping for {interval} seconds after sending request number: {i}")
    time.sleep(interval)


sqsRes = boto3.resource('sqs')
queue = sqsRes.Queue(sqsQueueUrl)

time_lst = []

j = 0
for j in range(num_of_requests):
    
    return_code = procs[j].wait()
    logger.info(f"Request number {j} finished with return code {return_code}.")
    if return_code == 0:
        normals.append(return_code)

        while True:
            try:
                start_time = time.perf_counter()
                received_messages = receive_messages(queue, 1, 20)
                print('received_messages',received_messages)
                for message in received_messages:
                    
                    Payload = json.loads(message.body)
                    output = json.loads(Payload['Message'])['parameters']['image_url']
                    print('output',output)

                    image_bucket, image_key = get_bucket_and_key(output)
                    time.sleep(1)
                    image_object = s3_resource.Object(image_bucket, image_key)
                    image = image_object.get()["Body"].read()
                    print('time spent test', j, time.perf_counter() - start_time)
                    time_lst.append(time.perf_counter() - start_time)
                    delete_message(message)
                break
            except Exception as e:
                print(e)
                continue
            
        

print('time_lst',time_lst)
            

        


#     else:
#         abnormals.append(return_code)

# print('请求次数：',num_of_requests)
# print('不正常响应次数：', len(abnormals))
# print('正常响应次数：', len(normals))

