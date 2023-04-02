DOCKER_COMPOSE_PATH = "tests/docker/docker-compose.yml"


def run_tool_in_container(c, env, profile, project_name, tool):
    c.run(
        (
            f"docker compose "
            f"-p {project_name} "
            f"--profile {profile} "
            f"-f {DOCKER_COMPOSE_PATH} "
            f"up "
            f"--exit-code-from {tool} "
            f"{tool}"
        ),
        env=env,
    )
