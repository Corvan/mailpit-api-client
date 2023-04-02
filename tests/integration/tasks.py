import pathlib

DOCKER_COMPOSE_PATH = "tests/docker/docker-compose.yml"


def start_mailpit_container(c, env, profile, project_name):
    c.run(
        (
            f"docker compose "
            f"-p {project_name} "
            f"--profile {profile} "
            f"-f {DOCKER_COMPOSE_PATH} "
            f"up "
            f"mailpit "
            f"-d"
        ),
        env=env,
    )


def stop_mailpit_container(c, env, profile, project_name):
    c.run(
        (
            f"docker compose "
            f"-p {project_name} "
            f"--profile {profile} "
            f"-f tests/docker/docker-compose.yml "
            f"stop "
            f"mailpit "
        ),
        env=env,
    )


def run_test_in_container(
    c, env: dict, profile: str, project_name: str, path: pathlib.Path
):
    c.run(
        (
            f"docker compose "
            f"-p {project_name} "
            f"--profile {profile} "
            f"-f {DOCKER_COMPOSE_PATH} "
            f"up "
            f"--exit-code-from integration "
            f"integration"
        ),
        env=env,
    )


def run_test(c, env, profile, project_name, test: pathlib.Path):
    start_mailpit_container(c, env, profile, project_name)
    try:
        run_test_in_container(c, env, profile, project_name, test)
    finally:
        stop_mailpit_container(c, env, profile, project_name)
