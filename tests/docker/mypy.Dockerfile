ARG python_version

FROM python:$python_version

RUN apt-get update && apt-get upgrade
RUN apt-get install -y python3-mypy
RUN pip install dataclasses-json httpx
