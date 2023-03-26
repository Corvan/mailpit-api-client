ARG python_version

FROM python:$python_version

RUN --mount=type=cache,target=/var/cache/apt <<EOF
set -e
apt-get update
apt-get upgrade -y
apt-get install -y python3-mypy
pip install dataclasses-json httpx
EOF
