import tomli
from invoke import task

PROJECT_NAME = "mailpit-api-client"
DOCKER_COMPOSE_PATH = "tests/docker/docker-compose.yml"


def read_pyproject_toml():
    with open("pyproject.toml", "rb") as fp:
        config = tomli.load(fp)
    return config["tool"]["invoke"]["test"]


@task
def unittest(c):
    config = read_pyproject_toml()
    profile = "unittest"
    for python_version in config["python_versions"]:
        project_name = f"{PROJECT_NAME}-{python_version}"
        env = {"PYTHON_VERSION": python_version}

        c.run(
            (
                f"docker-compose -p {project_name} "
                f"--profile {profile} -f {DOCKER_COMPOSE_PATH} up black"
            ),
            env=env,
        )

        c.run(
            (
                f"docker-compose -p {project_name} "
                f"--profile {profile} -f {DOCKER_COMPOSE_PATH} up lint"
            ),
            env=env,
        )

        c.run(
            (
                f"docker-compose -p {project_name } "
                f"--profile {profile} -f tests/docker/docker-compose.yml up mypy"
            ),
            env=env,
        )

        c.run(
            (
                f"docker-compose -p {project_name} "
                f"--profile {profile} -f tests/docker/docker-compose.yml up unittest"
            ),
            env=env,
        )


@task
def unittest_build(c):
    profile = "unittest"
    for python_version in ["3.9", "3.10", "3.11"]:
        project_name = f"{PROJECT_NAME}-{python_version}"
        env = {"PYTHON_VERSION": python_version}

        c.run(
            (
                f"docker-compose -p {project_name} "
                f"--profile {profile} -f {DOCKER_COMPOSE_PATH} build"
            ),
            env=env,
        )
