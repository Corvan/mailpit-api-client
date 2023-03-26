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
        project_name = f"{PROJECT_NAME}-{python_version.replace('.', '')}"
        env = {"PYTHON_VERSION": python_version}

        c.run(
            (
                f"docker compose "
                f"-p {project_name} "
                f"--profile {profile} "
                f"-f {DOCKER_COMPOSE_PATH} "
                f"up "
                f"--exit-code-from black "
                f"black"
            ),
            env=env,
        )

        c.run(
            (
                f"docker compose "
                f"-p {project_name} "
                f"--profile {profile} "
                f"-f {DOCKER_COMPOSE_PATH} "
                f"up "
                f"--exit-code-from lint "
                f"lint"
            ),
            env=env,
        )

        c.run(
            (
                f"docker compose "
                f"-p {project_name} "
                f"--profile {profile} "
                f"-f tests/docker/docker-compose.yml "
                f"up "
                f"--exit-code-from mypy "
                f"mypy"
            ),
            env=env,
        )

        c.run(
            (
                f"docker compose "
                f"-p {project_name} "
                f"--profile {profile} "
                f"-f tests/docker/docker-compose.yml "
                f"up "
                f"--exit-code-from unittest "
                f"unittest"
            ),
            env=env,
        )


@task
def unittest_build(c):
    profile = "unittest"
    config = read_pyproject_toml()
    for python_version in config["python_versions"]:
        project_name = f"{PROJECT_NAME}-{python_version.replace('.', '')}"
        env = {"PYTHON_VERSION": python_version}

        c.run(
            (
                f"docker-compose -p {project_name} "
                f"--profile {profile} -f {DOCKER_COMPOSE_PATH} build"
            ),
            env=env,
        )
