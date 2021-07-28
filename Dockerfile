FROM amazon/aws-lambda-python:3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .
RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["/opt/venv/bin/uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
