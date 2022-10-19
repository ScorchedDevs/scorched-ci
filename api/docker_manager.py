import docker
import logging
import requests
from config import ConfigEnv
from io import BytesIO


class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.config_env = ConfigEnv

    def build_docker_image(self, repo_name, docker_tag, dockerfile_path, latest):

        with open(dockerfile_path, encoding="utf-8") as file_:
            dockerfile = file_.read()
        encoded_dockerfile = BytesIO(dockerfile.encode("utf-8"))

        if latest:
            self.client.images.build(
                fileobj=encoded_dockerfile,
                dockerfile=dockerfile_path,
                tag=f"{repo_name}:latest",
                buildargs={"tag": f"{repo_name}:latest"},
            )

        image = self.client.images.build(
            fileobj=encoded_dockerfile,
            dockerfile=dockerfile_path,
            tag=f"{repo_name}:{docker_tag}",
            buildargs={"tag": f"{repo_name}:latest"},
        )

        return image[0]

    def docker_login(self, username, password):

        return self.client.login(username=username, password=password)

    def push_image_to_dockerhub(self, image, latest):

        if latest:
            latest_tag = image.tags[0].split(":")[0]
            for line in self.client.api.push(
                f"{latest_tag}:latest", stream=True, decode=True
            ):
                logging.info(line["status"]) if "status" in line else line

        for line in self.client.api.push(f"{image.tags[0]}", stream=True, decode=True):
            logging.info(line["status"]) if "status" in line else line

    def get_tag_list(self, repo_name):

        url = f"https://registry.hub.docker.com/v2/repositories/{repo_name}/tags?page_size=1024"

        response = requests.get(url)

        return response.json()["results"]
