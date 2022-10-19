from os import getenv
from varname import nameof


class ConfigEnv:
    # repo_name = getenv("REPO_NAME")
    # github_token = getenv("TOKEN")
    # docker_username = getenv("DOCKER_USERNAME")
    # docker_password = getenv("DOCKER_PASSWORD")
    # github_ref = getenv("GITHUB_REF")
    

    repo_name = "ryuunosukeds3/test_repository"
    github_token = getenv("TOKEN")
    docker_username = "ryuunosukeds3"
    docker_password = "Torpedo@223"
    github_ref = "refs/tags/1.1.1"


    def validate_release_envs(self):
        wrong_variables = list()

        if not self.repo_name:
            wrong_variables.append(nameof(self.repo_name).upper())

        if not self.github_token:
            wrong_variables.append(nameof(self.github_token).upper())

        variables_list_string = ", ".join(wrong_variables)

        if wrong_variables:
            raise SystemExit(f"Variables {variables_list_string} are not declared as environment variables in your github action yml file")

    def validate_docker_envs(self):
        wrong_variables = list()

        if not self.repo_name:
            wrong_variables.append(nameof(self.repo_name).upper())

        if not self.docker_username:
            wrong_variables.append(nameof(self.docker_username).upper())

        if not self.docker_password:
            wrong_variables.append(nameof(self.docker_password).upper())

        if not self.github_ref:
            wrong_variables.append(nameof(self.github_ref).upper())

        variables_list_string = ", ".join(wrong_variables)

        if wrong_variables:
            raise SystemExit(f"Variables {variables_list_string} are not declared as environment variables in your github action yml file")