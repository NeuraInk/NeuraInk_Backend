import os
import uvicorn
from fastapi import File, UploadFile, Form, Request, Depends
from fastapi import FastAPI
import json
from pydantic import BaseModel
import boto3

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

app = FastAPI(
    title="CycleGAN Test",
    description="""Port 8000""",
    version="0.0.0.0"
)

s3_client = boto3.client('s3')

def download_dir(prefix, local, bucket, client=s3_client):
    """
    params:
    - prefix: pattern to match in s3
    - local: local path to folder in which to place files
    - bucket: s3 bucket with target contents
    - client: initialized s3 client object
    """
    keys = []
    dirs = []
    next_token = ''
    base_kwargs = {
        'Bucket':bucket,
        'Prefix':prefix,
    }
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != '':
            kwargs.update({'ContinuationToken': next_token})
        results = client.list_objects_v2(**kwargs)
        contents = results.get('Contents')
        for i in contents:
            k = i.get('Key')
            if k[-1] != '/':
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get('NextContinuationToken')
    for d in dirs:
        dest_pathname = os.path.join(local, d)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(local, k)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        client.download_file(bucket, k, dest_pathname)

def upload_to_s3(file_path, bucket_name, object_name):
    """
    Upload file to S3 modified with rename upload file with the object_name
    :param file_path: Specify the file name, (the current setting is the file path).
    :param bucket_name: Specify the bucket name, eg. 'aai-test-company'
    :return: 3 different file locations for further access (s3_url,arn,object_url).
    """
    s3 = boto3.resource('s3')
    # with open(file_path, "rb") as f:
    # print(file_path)
        # s3.upload_fileobj(f.seek(0), bucket_name, object_name)
    print(object_name)
    s3.Bucket(bucket_name).put_object(Key=object_name, Body=file_path)
    s3_url = 's3://{}/{}'.format(bucket_name, object_name)
    arn = 'arn:aws:s3:::{}/{}'.format(bucket_name, object_name)
    object_url = 'https://{}.s3.amazonaws.com/{}'.format(bucket_name, object_name)
    return s3_url, arn, object_url

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        print(e)
        return False
    return True

class bk(BaseModel):
    file_path: str
    file_name: str
    bucket_name: str

# @app.get('/')
# def read_root():
#     return {'message': 'Welcome from the API'}

# @app.post('/process/')
# def get_tem_image(body: bk):
#
#     s3 = boto3.client('s3')
#     tmp = './tmp/'
#     if os.path.exists(os.path.dirname(tmp)):
#         os.system('rm -rf {}'.format(tmp))
#     os.mkdir(tmp)
#     s3.download_file(body.bucket_name, body.file_path + body.file_name, tmp + body.file_name)
#
#     command = "python test.py --dataroot {} --name {} --results_dir {} --gpu_ids -1 --model test --no_dropout --load_size {} --preprocess scale_width --crop_size {} --display_winsize {}"
#     dataroot = tmp
#     name = "inkwash"
#     results_dir = tmp
#     load_size = "512"
#     crop_size = "512"
#     display_winsize = "512"
#
#     os.system(command.format(dataroot,name,results_dir,load_size,crop_size,display_winsize))
#
#     print("\n-----------------------------------\n")
#     result_path = tmp + "inkwash/test_latest/images"
#     files = [f for f in os.listdir(result_path) if os.path.isfile(os.path.join(result_path, f))]
#     print(files)
#     print("\n-----------------------------------\n")
#     for file in files:
#         file_path = result_path + '/' + file
#         print(file)
#         obj_name = 'result/' + file
#         # s3_url, arn, object_url = upload_to_s3(file, "neuraink", file)
#         upload_file(file_path, body.bucket_name, obj_name)
#         # print(upload_to_s3(file, "neuraink", file))
#         print("\n")
#     print("\n-----------------------------------\n")
#
#     # os.system('rm -rf {}'.format(tmp))
#
#     return {"message": "CycleGan Success",
#             "error": False,
#             "success": True,
#             "data": {
#                 "s3_url": 's3://{}/{}'.format(body.bucket_name, obj_name)
#                 }
#         }

def handler(event, context):
    if event['task'] == 'welcome':

        result = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Welcome from the API",
                "error": False,
                "success": True,
            })
        }

        return result

    s3 = boto3.client('s3')
    tmp = './tmp/'
    if os.path.exists(os.path.dirname(tmp)):
        os.system('rm -rf {}'.format(tmp))
    os.mkdir(tmp)
    s3.download_file(event['bucket_name'], event['file_path'] + event['file_name'], tmp + event['file_name'])

    command = "python test.py --dataroot {} --name {} --results_dir {} --gpu_ids -1 --model test --no_dropout --load_size {} --preprocess scale_width --crop_size {} --display_winsize {}"
    dataroot = tmp
    name = "inkwash"
    results_dir = tmp
    load_size = "512"
    crop_size = "512"
    display_winsize = "512"

    os.system(command.format(dataroot, name, results_dir, load_size, crop_size, display_winsize))

    print("\n-----------------------------------\n")
    result_path = tmp + "inkwash/test_latest/images"
    files = [f for f in os.listdir(result_path) if os.path.isfile(os.path.join(result_path, f))]
    print(files)
    print("\n-----------------------------------\n")
    for file in files:
        file_path = result_path + '/' + file
        print(file)
        obj_name = 'result/' + file
        # s3_url, arn, object_url = upload_to_s3(file, "neuraink", file)
        upload_file(file_path, event['bucket_name'], obj_name)
        # print(upload_to_s3(file, "neuraink", file))
        print("\n")
    print("\n-----------------------------------\n")

    # os.system('rm -rf {}'.format(tmp))

    result = {
        "statusCode":200,
        "headers":{
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "CycleGan Success",
            "error": False,
            "success": True,
            "s3_url": 's3://{}/{}'.format(event['bucket_name'], obj_name)
            })
        }

    return result