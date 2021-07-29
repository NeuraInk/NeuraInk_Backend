import json
import boto3
import urllib.request
import io
import numpy as np
from PIL import Image

def lambda_handler(event, context):
    file_name = event['Records'][0]['s3']['object']['key']
    req = urllib.request.Request(url=f'https://s3.amazonaws.com/{file_name}')
    with urllib.request.urlopen(req) as f:
        send(file_name, f.read())
    

def send(file_name, payload):
    endpoint_name = '123-456-789' # Modify this to your endpoint
    runtime = boto3.client('runtime.sagemaker')
    response = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='image/*', Body=payload)
    
    new_image = Image.fromarray(np.array(json.loads(response['Body'].read()), dtype='uint8'))
    buffer = io.BytesIO()
    new_image.save(buffer, "JPEG")
    buffer.seek(0)  # rewind pointer back to start
    s3 = boto3.client('s3')
    original_name = file_name.split(".")[0]
    original_name = original_name.split("/")[1]
    
    
    s3.put_object(
        Bucket="your_bucket",
        Key=f"public/output/output_{original_name}.jpeg",
        Body=buffer,
        ContentType='image/jpeg',
        ACL= 'public-read',
    )