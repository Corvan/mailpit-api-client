ARG python_version

FROM python:$python_version

RUN --mount=type=cache,target=/var/cache/apt <<EOF
set -e
apt-get update
apt-get upgrade -y
pip -qq install dataclasses_json httpx respx
EOF