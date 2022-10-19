import logging
from api import DockerManager
from config import ConfigEnv
from packaging import version


class DockerImageCreator:
    def __init__(self):
        self.docker_manager = DockerManager()
        self.config_env = ConfigEnv()

    def create_and_push_image(self):

        self.config_env.validate_docker_envs()
        logging.info("Trying to login into Docker Hub")
        login = self.docker_manager.docker_login(
            self.config_env.docker_username, self.config_env.docker_password
        )
        logging.info(login["Status"])
        tag = self.get_tag(self.config_env.github_ref)
        latest_string = "also"
        latest = self.check_if_tag_is_latest(tag, self.config_env.repo_name)
        if not latest:
            latest_string = "not"
        logging.info("Tag %s is %s latest tag", tag, latest_string)
        logging.info("Building docker image")
        docker_image = self.docker_manager.build_docker_image(
            self.config_env.repo_name, tag, "/Dockerfile", latest
        )
        logging.info("Docker image %s successfully created", docker_image.tags[0])
        logging.info("Pushing image(s) to Docker Hub")
        self.docker_manager.push_image_to_dockerhub(
            docker_image, latest
        )

    def get_tag(self, github_ref):

        if "tags" not in github_ref:
            raise SystemExit("Target is not a tag.")

        tag = github_ref.replace("refs/tags/", "")

        return tag

    def check_if_tag_is_latest(self, tag, repo_name):
        current_latest_tag = self.get_latest_tag(repo_name)

        if current_latest_tag:
            return version.parse(tag) > version.parse(current_latest_tag)
        else:
            return None

    def get_latest_tag(self, repo_name):

        results = self.docker_manager.get_tag_list(repo_name)

        if results:

            sorted_majors = sorted(
                results,
                key=lambda result: int(result["name"].split(".")[0].replace("v", "")),
                reverse=True,
            )
            sorted_minors = sorted(
                sorted_majors,
                key=lambda sorted_major: int(sorted_major["name"].split(".")[1]),
                reverse=True,
            )
            sorted_versions = sorted(
                sorted_minors,
                key=lambda sorted_minor: int(sorted_minor["name"].split(".")[2]),
                reverse=True,
            )

            return sorted_versions[0]["name"]

        else:
            return None
