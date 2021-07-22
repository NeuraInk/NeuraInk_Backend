FROM amazon/aws-lambda-python:3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY

RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["backend.handler"]

#CMD ["/opt/venv/bin/uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]




#FROM condaforge/mambaforge:4.9.2-5 as conda
#
#RUN mkdir /app
#WORKDIR /app
#COPY . .
##COPY conda-linux-64.lock .
#
### not sure why we need these lines but errors otherwise
### https://github.com/docker/buildx/issues/426
#RUN export DOCKER_BUILDKIT=0
#RUN export COMPOSE_DOCKER_CLI_BUILD=0
#ENV APP_ENV=docker
#
## Make env from lockfile and delete tarballs
##RUN mamba create --name ds --file conda-linux-64.lock && \
##    conda clean -afy
#
### install pip dependences and aai api
#RUN conda run -n ds python -m pip install -r requirements.txt
###RUN conda run -n aai_cpu python -m pip install .
#
#SHELL ["conda", "run", "-n", "ds", "/bin/bash", "-c"]
#
#COPY backend.py .
#EXPOSE 8000
#
#ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ds", "python", "backend.py"]