import logging

import invoke as inv

DOCKER_COMPOSE_PATH = "tests/docker/docker-compose.yml"
logger = logging.getLogger("test_runner")


def start_mailpit_container(c: inv.Context, env, profile, project_name):
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


def run_tests(c: inv.Context, env: dict, profile: str, project_name: str):
    logger.info("run test in container environment")
    try:
        command = (
            f"docker compose "
            f"-p {project_name} "
            f"--profile {profile} "
            f"-f {DOCKER_COMPOSE_PATH} "
            f"up "
            f"--exit-code-from integration "
            f"integration"
        )

        logger.debug(f"command: `{command}`")
        c.run(command, env=env, pty=True)
    except inv.Failure as fe:
        logger.error("An error occurred on running test in container enviroment")
        logger.exception(fe)
        raise fe
