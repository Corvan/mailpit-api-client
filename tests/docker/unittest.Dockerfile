ARG python_version

FROM python:$python_version

RUN apt-get update && apt-get upgrade
RUN pip -qq install dataclasses_json httpx respx