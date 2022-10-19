from app import ReleasesCreator, DockerImageCreator
from config import config_logger

config_logger()


def release_major():
    release_manager = ReleasesCreator()
    release_manager.create_new_release(major=True)


def release_minor():
    release_manager = ReleasesCreator()
    release_manager.create_new_release(minor=True)


def release_patch():
    release_manager = ReleasesCreator()
    release_manager.create_new_release(patch=True)

def create_and_push_docker_image():
    docker_image_creator = DockerImageCreator()
    docker_image_creator.create_and_push_image()


create_and_push_docker_image()