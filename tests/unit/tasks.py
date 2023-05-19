import logging

import invoke as inv

DOCKER_COMPOSE_PATH = "tests/docker/docker-compose.yml"
logger = logging.getLogger("test_runner")


def run_tool_in_container(
    c: inv.Context, env: dict, profile: str, project_name: str, tool: str
):
    command = (
        f"docker compose "
        f"-p {project_name} "
        f"--profile {profile} "
        f"-f {DOCKER_COMPOSE_PATH} "
        f"up "
        f"--exit-code-from {tool} "
        f"{tool}"
    )
    logger.debug(f"command: {command}")
    c.run(command, env=env, pty=True)
