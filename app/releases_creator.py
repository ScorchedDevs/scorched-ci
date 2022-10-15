import logging
from api import GithubManager
from .migrate_releases import MigrateReleases


class ReleasesCreator:
    def __init__(self):
        self.github_manager = GithubManager()
        self.migrate_releases = MigrateReleases()

    def create_new_release(self, repo_name=None, major=False, minor=False, patch=False):

        repo = self.github_manager.get_github_repository(repo_name)
        logging.info("Getting repository")
        logging.info("Merging default branch into main")
        merge_commit = self.github_manager.merge_default_branch_into_main(repo)
        logging.info("Merge commit: %s", merge_commit.url)
        new_tag = self.calculate_new_tag(repo, major, minor, patch)
        description = self.create_release_description(repo)
        logging.info("Creating a new release")
        created_release = self.github_manager.create_new_tag_and_release(
            repo, new_tag, description
        )
        logging.info(
            "New release and tag created: %s %s",
            created_release.title,
            created_release.url,
        )
        self.github_manager.replace_changelog_file(repo)
        logging.info("Changelog changed to template")

    def calculate_new_tag(self, repo, major, minor, patch):
        latest_tag = self.github_manager.get_latest_tag(repo)

        if not latest_tag:
            latest_tag = "v0.0.0"

        if "-" in latest_tag:
            self.migrate_releases.migrate_releases(repo)
            latest_tag = self.github_manager.get_latest_tag(repo)

        split_tag = latest_tag.split(".")

        major_number = split_tag[0]
        minor_number = split_tag[1]
        patch_number = split_tag[2]

        if major:
            major_number = major_number.replace("v", "")
            major_number = int(major_number) + 1
            major_number = "v" + str(major_number)
            minor_number = "0"
            patch_number = "0"

        if minor:
            minor_number = str(int(minor_number) + 1)
            patch_number = "0"

        if patch:
            patch_number = str(int(patch_number) + 1)

        new_tag_tuple = (major_number, minor_number, patch_number)

        new_tag = ".".join(new_tag_tuple)

        return new_tag

    def create_release_description(self, repo):

        description = ""

        changelog_content = self.github_manager.get_changelog_content(repo)
        split_changelog_file = (
            changelog_content.replace("\n", " ").replace("# Changelog", "").split("##")
        )
        split_changelog_file.pop(0)

        for section in split_changelog_file:
            if not "N/A" in section:

                changes = section.split(" -")
                title = changes[0].strip()
                description += f"## {title}\n"
                changes.pop(0)

                for change in changes:
                    description += f"  -{change.rstrip()}\n"

        if description == "":
            raise SystemExit("Empty Changelog")

        return description
