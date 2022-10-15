import logging
from api import GithubManager


class MigrateReleases:
    def __init__(self):
        self.github_manager = GithubManager()

    def migrate_releases(self, repo):

        releases = self.github_manager.get_repository_releases(repo)
        self.delete_and_recreate_wrong_releases(repo, releases)

    def delete_and_recreate_wrong_releases(self, repo, releases):

        deleted_release = None

        for release in releases:
            if "-" in release.tag_name:
                created_release = self.replace_tag_and_release(repo, release)
                deleted_release = self.github_manager.delete_release_and_tag(repo, release)

                logging.info(
                    "Release %s replaced by release %s %s",
                    deleted_release.title,
                    created_release.title,
                    created_release.url,
                )

    def replace_tag_and_release(self, repo, release):

        new_tag = release.tag_name.replace("-", ".")
        release_description = release.body
        commit_sha = release.raw_data["target_commitish"]
        created_release = self.github_manager.create_new_tag_and_release(
            repo, new_tag, release_description, commit_sha=commit_sha
        )

        return created_release
