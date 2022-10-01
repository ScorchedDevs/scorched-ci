from github import Github


class GithubManager:
    def __init__(self):

        self.github = Github("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")

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

    def create_new_tag_and_release(self, repo, new_tag, release_description):

        commit_sha = repo.get_branch("main").commit.sha
        repo.create_git_tag_and_release(
            tag=new_tag,
            tag_message="Tag criada automaticamente pelo Scorched CI",
            release_name=new_tag,
            release_message=release_description,
            type="commit",
            object=commit_sha,
        )

    def replace_changelog_file(self, repo):

        changelog_file = repo.get_contents("CHANGELOG.md")
        repo.delete_file(
            changelog_file.path,
            "Deletando changelog populado",
            changelog_file.sha,
            branch="main",
        )
        with open("changelog_template.md", encoding="utf-8") as changelog_template:
            repo.create_file(
                "CHANGELOG.md",
                "Recriando changelog a partir do template",
                changelog_template.read(),
                branch="main",
            )
