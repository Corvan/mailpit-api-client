import logging
import pathlib

import invoke as inv

DOCKER_COMPOSE_PATH = "tests/docker/docker-compose.yml"


def start_mailpit_container(c: inv.Context, env, profile, project_name):
    logger = logging.getLogger("test_runner.integration.tasks.start_mailpit_container")
    command = (
        f"docker compose "
        f"-p {project_name} "
        f"--profile {profile} "
        f"-f {DOCKER_COMPOSE_PATH} "
        f"up "
        f"mailpit "
        f"-d"
    )

    logger.info("Starting mailpit container")
    logger.debug(f"command: `{command}`")
    c.run(command, env=env, pty=True)


def stop_mailpit_container(c: inv.Context, env: dict, profile: str, project_name: str):
    logger = logging.getLogger("test_runner.integration.tasks.stop_mailpit_container")
    command = (
        f"docker compose "
        f"-p {project_name} "
        f"--profile {profile} "
        f"-f tests/docker/docker-compose.yml "
        f"stop "
        f"mailpit "
    )

    logger.info("Stopping mailpit container")
    logger.debug(f"command: `{command}`")
    c.run(command, env=env, pty=True)


def run_test_in_container(
    c, env: dict, profile: str, project_name: str, path: pathlib.Path
):
    logger = logging.getLogger("test_runner.integration.tasks.run_tests_in_container")
    command = (
        f"docker compose "
        f"-p {project_name} "
        f"--profile {profile} "
        f"-f {DOCKER_COMPOSE_PATH} "
        f"up "
        f"integration"
    )

    logger.info(f'running test file `{path}` in container "integration"')
    logger.debug(f"command: `{command}`")
    c.run(command, env=env, pty=True)


def run_test(
    c: inv.Context, env: dict, profile: str, project_name: str, test: pathlib.Path
):
    logger = logging.getLogger("test_runner.integration.tasks.run_test")
    logger.info("run test in container environment")
    try:
        start_mailpit_container(c, env, profile, project_name)
        run_test_in_container(c, env, profile, project_name, test)
    except Exception as e:
        logger.error("An error occurred on running test in container enviroment")
        logger.exception(e)
        raise e
    finally:
        stop_mailpit_container(c, env, profile, project_name)
