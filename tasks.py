import pathlib

import tomli
import invoke as inv
import tests.unit.tasks as ut
import tests.integration.tasks as it

PROJECT_NAME = "mailpit-api-client"
DOCKER_COMPOSE_PATH = "tests/docker/docker-compose.yml"


def read_pyproject_toml():
    with open("pyproject.toml", "rb") as fp:
        config = tomli.load(fp)
    return config["tool"]["invoke"]["test"]


def build_containers(c, profile: str):
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


@inv.task
def unit(c):
    config = read_pyproject_toml()
    profile = "unittest"
    tools = ["black", "lint", "mypy", "unittest"]

    for python_version in config["python_versions"]:
        project_name = f"{PROJECT_NAME}-{python_version.replace('.', '')}"
        env = {"PYTHON_VERSION": python_version}

        for tool in tools:
            ut.run_tool_in_container(c, env, profile, project_name, tool)


@inv.task
def integration(c):
    config = read_pyproject_toml()
    profile = "integration"
    path = pathlib.Path("tests/integration")
    for file in path.iterdir():
        if file.name.startswith("test"):
            for python_version in config["python_versions"]:
                project_name = f"{PROJECT_NAME}-{python_version.replace('.', '')}"
                print(file)
                env = {
                    "PYTHON_VERSION": python_version,
                    "TEST_FILE": str(file),
                    "PYTHONTRACEMALLOC": "1",
                }

                it.run_test(c, env, profile, project_name, file)


@inv.task
def unittest_build(c):
    profile = "integration"
    build_containers(c, profile)


@inv.task
def integration_build(c):
    profile = "integration"
    build_containers(c, profile)
