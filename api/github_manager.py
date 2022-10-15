from os import getenv
from github import Github
import requests


class GithubManager:
    def __init__(self):

        self.token = getenv("TOKEN")
        self.github = Github(self.token)

    def get_github_repository(self, repo_name):

        repo = self.github.get_repo(repo_name)

        return repo

    def get_latest_tag(self, repo):

        tag = list(repo.get_tags())[0].name if list(repo.get_tags()) else None

        return tag

    def get_changelog_content(self, repo):

        changelog_file = repo.get_contents("CHANGELOG.md")
        changelog_content = changelog_file.decoded_content.decode()

        return changelog_content

    def merge_default_branch_into_main(self, repo):

        default_branch = self.get_default_branch_name(repo)

        head = repo.get_branch(default_branch)

        merge_commit = repo.merge(
            "main", head.commit.sha, f"Merging {default_branch} into main branch"
        )

        return merge_commit

    def create_new_tag_and_release(
        self, repo, new_tag, release_description, commit_sha=None
    ):

        if not commit_sha:
            commit_sha = repo.get_branch("main").commit.sha

        created_release = repo.create_git_tag_and_release(
            tag=new_tag,
            tag_message="Tag created automatically by Scorched CI",
            release_name=new_tag,
            release_message=release_description,
            type="commit",
            object=commit_sha,
        )

        return created_release

    def replace_changelog_file(self, repo):

        changelog_file = repo.get_contents("CHANGELOG.md")
        repo.delete_file(
            changelog_file.path,
            "Deleting pupulated changelog file",
            changelog_file.sha,
            branch="develop",
        )
        with open("changelog_template.md", encoding="utf-8") as changelog_template:
            repo.create_file(
                "CHANGELOG.md",
                "Recreating changelog file from changelog template",
                changelog_template.read(),
                branch="develop",
            )

    def get_default_branch_name(self, repo):

        return repo.default_branch

    def get_repository_releases(self, repo):

        return list(repo.get_releases())

    def delete_release_and_tag(self, repo, release):

        url_release = (
            f"https://api.github.com/repos/{repo.full_name}/releases/{release.id}"
        )
        url_tag = f"https://api.github.com/repos/{repo.full_name}/git/refs/tags/{release.tag_name}"

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {self.token}",
        }

        requests.delete(url_release, headers=headers, timeout=60)
        requests.delete(url_tag, headers=headers, timeout=60)

        return release
