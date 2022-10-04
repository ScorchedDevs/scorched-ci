# pylint: disable=too-few-public-methods, invalid-name, no-self-argument, redefined-builtin, too-many-arguments
from pytest_mock import MockerFixture
from releases_manager import ReleasesManager


class FakeRepo: # pragma: no cover
    def get_branch(branch_name):
        class branch:
            class commit:
                sha = "somecommitsha"

        return branch

    def create_git_tag_and_release(
        tag, tag_message, release_name, release_message, type, object
    ): 
        pass

    def get_contents(changelog_file):
        class file:
            path = "some/path"
            sha = "somecommitsha"

        return file

    def delete_file(path, commit_message, sha, branch):
        pass

    def create_file(file_name, commit_message, file_content, branch):
        pass


fake_repo_name = "SomeRepo"
fake_tag = "v1-0-0"
fake_changelog = """
    # Changelog

    ## Novas funcionalidades

    - adding tests

    ## Melhorias

    - N/A

    ## Correções

    - N/A

    ## Quebra de compatibilidade

    - N/A
"""
fake_repo = FakeRepo


def test_release_major(mocker: MockerFixture) -> None:

    get_github_repository_mock = mocker.patch(
        "github_manager.GithubManager.get_github_repository", return_value=fake_repo
    )
    get_latest_tag_mock = mocker.patch(
        "github_manager.GithubManager.get_latest_tag", return_value=fake_tag
    )
    get_changelog_content_mock = mocker.patch(
        "github_manager.GithubManager.get_changelog_content",
        return_value=fake_changelog,
    )
    merge_develop_into_main_mock = mocker.patch(
        "github_manager.GithubManager.merge_develop_into_main"
    )
    create_new_tag_and_release_mock = mocker.patch(
        "github_manager.GithubManager.create_new_tag_and_release"
    )
    replace_changelog_file_mock = mocker.patch(
        "github_manager.GithubManager.replace_changelog_file"
    )

    releases_manager = ReleasesManager()
    releases_manager.create_new_release(repo_name=fake_repo_name, major=True)

    get_github_repository_mock.assert_called_once_with(fake_repo_name)
    get_latest_tag_mock.assert_called_once_with(fake_repo)
    get_changelog_content_mock.assert_called_once_with(fake_repo)
    merge_develop_into_main_mock.assert_called_once()
    create_new_tag_and_release_mock.assert_called_once()
    replace_changelog_file_mock.assert_called_once()

    assert (
        releases_manager.calculate_new_tag(
            fake_tag, major=True, minor=False, patch=False
        )
        == "v2-0-0"
    )
    assert (
        releases_manager.create_release_description(fake_repo)
        == "## Novas funcionalidades\n  - adding tests\n"
    )


def test_release_minor(mocker: MockerFixture) -> None:

    get_github_repository_mock = mocker.patch(
        "github_manager.GithubManager.get_github_repository", return_value=fake_repo
    )
    get_latest_tag_mock = mocker.patch(
        "github_manager.GithubManager.get_latest_tag", return_value=fake_tag
    )
    get_changelog_content_mock = mocker.patch(
        "github_manager.GithubManager.get_changelog_content",
        return_value=fake_changelog,
    )
    merge_develop_into_main_mock = mocker.patch(
        "github_manager.GithubManager.merge_develop_into_main"
    )
    create_new_tag_and_release_mock = mocker.patch(
        "github_manager.GithubManager.create_new_tag_and_release"
    )
    replace_changelog_file_mock = mocker.patch(
        "github_manager.GithubManager.replace_changelog_file"
    )

    releases_manager = ReleasesManager()
    releases_manager.create_new_release(repo_name=fake_repo_name, minor=True)

    get_github_repository_mock.assert_called_once_with(fake_repo_name)
    get_latest_tag_mock.assert_called_once_with(fake_repo)
    get_changelog_content_mock.assert_called_once_with(fake_repo)
    merge_develop_into_main_mock.assert_called_once()
    create_new_tag_and_release_mock.assert_called_once()
    replace_changelog_file_mock.assert_called_once()

    assert (
        releases_manager.calculate_new_tag(
            fake_tag, major=False, minor=True, patch=False
        )
        == "v1-1-0"
    )
    assert (
        releases_manager.create_release_description(fake_repo)
        == "## Novas funcionalidades\n  - adding tests\n"
    )


def test_release_patch(mocker: MockerFixture) -> None:

    get_github_repository_mock = mocker.patch(
        "github_manager.GithubManager.get_github_repository", return_value=fake_repo
    )
    get_latest_tag_mock = mocker.patch(
        "github_manager.GithubManager.get_latest_tag", return_value=fake_tag
    )
    get_changelog_content_mock = mocker.patch(
        "github_manager.GithubManager.get_changelog_content",
        return_value=fake_changelog,
    )
    merge_develop_into_main_mock = mocker.patch(
        "github_manager.GithubManager.merge_develop_into_main"
    )
    create_new_tag_and_release_mock = mocker.patch(
        "github_manager.GithubManager.create_new_tag_and_release"
    )
    replace_changelog_file_mock = mocker.patch(
        "github_manager.GithubManager.replace_changelog_file"
    )

    releases_manager = ReleasesManager()
    releases_manager.create_new_release(repo_name=fake_repo_name, patch=True)

    get_github_repository_mock.assert_called_once_with(fake_repo_name)
    get_latest_tag_mock.assert_called_once_with(fake_repo)
    get_changelog_content_mock.assert_called_once_with(fake_repo)
    merge_develop_into_main_mock.assert_called_once()
    create_new_tag_and_release_mock.assert_called_once()
    replace_changelog_file_mock.assert_called_once()

    assert (
        releases_manager.calculate_new_tag(
            fake_tag, major=False, minor=False, patch=True
        )
        == "v1-0-1"
    )
    assert (
        releases_manager.create_release_description(fake_repo)
        == "## Novas funcionalidades\n  - adding tests\n"
    )
