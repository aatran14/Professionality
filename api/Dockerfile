#python version
FROM continuumio/miniconda3

#working directory
WORKDIR /code

#create conda environment
RUN conda create -n newenv python=3.11
SHELL [ "conda", "run", "-n", "newenv", "/bin/bash", "-c" ]
RUN conda config --append channels conda-forge

#copy requirements into working dir
COPY ./requirements.yml /code/requirements.yml

#install dependencies
RUN conda install --file /code/requirements.yml

#copy app into working dir
COPY ./app /code/app

#spin up container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]