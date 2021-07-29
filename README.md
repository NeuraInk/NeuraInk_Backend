# NeuraInk_Backend

The backend service of NeuraInk uses the [CycleGAN](https://junyanz.github.io/CycleGAN/) machine learning algorithm to implement the inkwash photo transformation.
 
### How to run on AWS EC2 Instance / Locally
1. Create an EC2 Instance (skip this step if you are running locally)
2. git clone the NeuraInk_Backend repo
3. Run `chmod +x ./setup.sh ./start.sh` to give executeable permissions to both bash files
4. Run `./setup.sh` to setup the virtual environment
5. Run `./start.sh` to start the backend services

### Deploy Machine Learning Model with AWS SageMaker
1. Create a jupyter notebook instance in SageMaker
2. Upload your model file as a ```tar.gz file``` to a S3 bucket.
3. Create an ```inference.py``` file as the entry point to your model. You can put it in the same folder as your notebook.
    - ```model_fn()``` function to create your model
    - ```input_fn()``` function to handle your input such as: ``` content_type='application/json' ``` and you can conduct preprocessing of your input data in here.
    - ```predict_fn()``` function will evaluate the input data that you processed with the model
    - ```output_fn()``` function could process the prediction output to your desired format, such as json.

4. Define an IAM role in the notebook instance.
5. Create a pytorch model in the notebook instance and deploy it with the instance type that you specified.

### Invoke AWS SageMaker Model Endpoint with Lambda Function
Once you ran the notebook instance, it will automatically create an endpoint for you. With that information, you can create a lambda function to invoke that endpoint. In our case, we used python 3.8 as our language for the lambda function.

On top of that, we also created an S3 trigger, so whenever a new picture is passed into the bucket that we specified, the lambda function will be called automatically and hence invoke our model endpoint.

![image](https://user-images.githubusercontent.com/38733111/127421153-3cb711e9-2860-43aa-81b8-bf2266cd438a.png)

In order to use specific Python libraries, we included layers for ```Pillow``` and ```NumPy``` through [Klayers](https://github.com/keithrozario/Klayers).

1. ```lambda_handler``` function will handle the event passed in. 
In our case, the event is a picture has been created in a S3 bucket. By examning the event structure, we could fetch the file name and use Python's ```urlib.request``` library to read the content.

2. ```send``` function will invoke the model endpoint and handle the output.
    - We will use ```boto3.client('runtime.sagemaker')``` to invoke the endpoint and get the response.
    - ```Image``` library could help us turn the response to an image.
    - Call ```s3.put_object``` to create the transformed image back to S3 bucket.

