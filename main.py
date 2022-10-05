from os import getenv
from app import ReleasesCreator
from config import config_logger

release_manager = ReleasesCreator()

config_logger()

repo_name = getenv("REPO_NAME")

def release_major():
    release_manager.create_new_release(repo_name=repo_name, major=True)


def release_minor():
    release_manager.create_new_release(repo_name=repo_name, minor=True)


def release_patch():
    release_manager.create_new_release(repo_name=repo_name, patch=True)
