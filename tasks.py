import itertools
import logging
import pathlib

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

import invoke as inv
import tests.unit.tasks as ut
import tests.integration.tasks as it
import logging518.config

PROJECT_NAME = "mailpit-api-client"
DOCKER_COMPOSE_PATH = "tests/docker/docker-compose.yml"

logging518.config.fileConfig("pyproject.toml")
namespace = inv.Collection()


def read_pyproject_toml():
    with open("pyproject.toml", "rb") as fp:
        config = toml.load(fp)
    return config["tool"]["invoke"]["test"]


def build_containers(c: inv.Context, profile: str):
    config = read_pyproject_toml()
    for python_version, debian_codename in itertools.product(
            config["python_versions"], config["debian_codenames"]
    ):
        project_name = f"{PROJECT_NAME}-{python_version.replace('.', '')}-{debian_codename}"
        env = {"PYTHON_VERSION": python_version, "DEBIAN_CODENAME": debian_codename}
        command = (
                f"docker-compose -p {project_name} "
                f"--profile {profile} -f {DOCKER_COMPOSE_PATH} build --pull"
            )
        print(command)
        c.run(
            command,
            env=env,
            pty=True,
        )


def run(c, logger, profile, debian_codename, python_version, tool):
    logger.info(f"running with Python {python_version}")
    logger.info(f"running with Debian {debian_codename}")
    logger.info(f"running with checker {tool}")
    project_name = f"{PROJECT_NAME}-{python_version.replace('.', '')}"
    env = {"PYTHON_VERSION": python_version, "DEBIAN_CODENAME": debian_codename}
    logger.debug(f"set environment variables to: {env}")
    ut.run_tool_in_container(c, env, profile, project_name, tool)


@inv.task
def checks(c: inv.Context):
    logger = logging.getLogger("test_runner.checks")
    logger.info("code checking started")

    config = read_pyproject_toml()
    profile = "checks"

    for python_version, debian_codename, tool in itertools.product(
            config["python_versions"], config["debian_codenames"], config["checkers"]
    ):
        run(c, logger, profile, debian_codename, python_version, tool)


@inv.task
def unit(c: inv.Context):
    logger = logging.getLogger("test_runner.unit")
    logger.info("unit testing started")

    config = read_pyproject_toml()
    profile = "unittest"
    tools = ["unittest"]

    for python_version, debian_codename, tool in itertools.product(
            config["python_versions"], config["debian_codenames"], tools
    ):
        run(c, logger, profile, debian_codename, python_version, tool)


@inv.task
def integration(c: inv.Context):
    logger = logging.getLogger("test_runner.integration")
    logger.info("integration testing started")
    config = read_pyproject_toml()
    profile = "integration"
    path = pathlib.Path("tests/integration")
    for python_version, debian_codename, file in itertools.product(
            config["python_versions"], config["debian_codenames"],  path.iterdir()
    ):
        logger.info(f"running with Python {python_version}")
        logger.info(f"running with Debian {debian_codename}")
        if file.name.startswith("test"):
            logger.info(f"running tests in file {file}")
            project_name = (f"{PROJECT_NAME}"
                            f"-{python_version.replace('.', '')}"
                            f"-{debian_codename}")
            env = {
                "PYTHON_VERSION": python_version,
                "TEST_FILE": str(file),
                "PYTHONTRACEMALLOC": "1",
                "DEBIAN_CODENAME": debian_codename,
            }
            logger.debug(f"set environment variables to: {env}")

            it.run_test(c, env, profile, project_name, file)


@inv.task
def build_checks(c: inv.Context):
    build_containers(c, profile="checks")


@inv.task
def build_unittest(c: inv.Context):
    build_containers(c, profile="unittest")


@inv.task
def build_integration(c: inv.Context):
    build_containers(c, profile="integration")


tests = inv.Collection("tests")
tests.add_task(checks)
tests.add_task(unit)
tests.add_task(integration)

docker = inv.Collection("docker")

build = inv.Collection("build")
build.add_task(build_checks, "checks")
build.add_task(build_integration, name="integration")
build.add_task(build_unittest, name="unit")

docker.add_collection(build)

namespace.add_collection(tests)
namespace.add_collection(docker)
