from os import getenv
from github import Github


class GithubManager:
    def __init__(self):

        token = getenv("TOKEN")
        self.github = Github(token)

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

        merge_commit = repo.merge("main", head.commit.sha, f"Merging {default_branch} into main branch")

        return merge_commit

    def create_new_tag_and_release(self, repo, new_tag, release_description):

        commit_sha = repo.get_branch("main").commit.sha
        created_release = repo.create_git_tag_and_release(
            tag=new_tag,
            tag_message="Tag criada automaticamente pelo Scorched CI",
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
            "Deletando changelog populado",
            changelog_file.sha,
            branch="develop",
        )
        with open("changelog_template.md", encoding="utf-8") as changelog_template:
            repo.create_file(
                "CHANGELOG.md",
                "Recriando changelog a partir do template",
                changelog_template.read(),
                branch="develop",
            )

    def get_default_branch_name(self, repo):

        return repo.default_branch
