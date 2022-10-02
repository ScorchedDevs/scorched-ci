from os import getenv
from releases_manager import ReleasesManager
from utils import Utils

release_manager = ReleasesManager()
utils = Utils()
utils.start_streaming_the_log()

repo_name = getenv("REPO_NAME")

def release_major():
    release_manager.create_new_release(repo_name=repo_name, major=True)


def release_minor():
    release_manager.create_new_release(repo_name=repo_name, minor=True)


def release_patch():
    release_manager.create_new_release(repo_name=repo_name, patch=True)
