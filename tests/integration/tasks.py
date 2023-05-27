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
        "--pull "
        f"mailpit "
        f"-d"
    )

    logger.info("Starting mailpit container")
    logger.debug(f"command: `{command}`")
    c.run(command, env=env, pty=True)


def stop_mailpit_container(c: inv.Context, env: dict, profile: str, project_name: str):
    stop_command = (
        f"docker compose "
        f"-p {project_name} "
        f"--profile {profile} "
        f"-f tests/docker/docker-compose.yml "
        f"stop "
        f"mailpit "
    )

    logger.info("Stopping mailpit container")
    logger.debug(f"command: `{stop_command}`")
    c.run(stop_command, env=env, pty=True)
    rm_command = (
        f"docker compose "
        f"-p {project_name} "
        f"--profile {profile} "
        f"-f tests/docker/docker-compose.yml "
        f"rm -f "
        f"mailpit "
    )

    logger.info("Stopping mailpit container")
    logger.debug(f"command: `{rm_command}`")
    c.run(rm_command, env=env, pty=True)


def run_tests(c: inv.Context, env: dict, profile: str, project_name: str):
    logger.info("run test in container environment")
    try:
        up_command = (
            f"docker compose "
            f"-p {project_name} "
            f"--profile {profile} "
            f"-f {DOCKER_COMPOSE_PATH} "
            f"up "
            "--pull "
            f"--exit-code-from integration "
            f"integration"
        )
        logger.debug(f"command: `{up_command}`")
        c.run(up_command, env=env, pty=True)
    except inv.Failure as fe:
        logger.error("An error occurred on running test in container enviroment")
        logger.exception(fe)
        raise fe
    finally:
        down_command = (
            f"docker compose "
            f"-p {project_name} "
            f"--profile {profile} "
            f"-f {DOCKER_COMPOSE_PATH} "
            f"down"
        )
        logger.debug(f"command: `{down_command}`")
        c.run(down_command, env=env, pty=True)
