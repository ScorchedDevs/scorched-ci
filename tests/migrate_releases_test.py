# pylint: disable=too-few-public-methods, invalid-name, no-self-argument, redefined-builtin, too-many-arguments, no-method-argument
from pytest_mock import MockerFixture
from app.migrate_releases import MigrateReleases


class Release: # pragma: no cover
    title = "v1-0-0"
    tag_name = "v1-0-0"
    body = """## Fixes\n - Test fixes"""
    raw_data = {"target_commitish": "somecommitsha"}
    id = 12345


class FakeRepo: # pragma: no cover
    full_name = "some/repo-name"

    # pragma: no cover
    def get_releases():
        pass


class CreatedRelease: # pragma: no cover
    title = "v1.0.0"
    url = "some url"


class DeletedRelease: # pragma: no cover
    title = "v1-0-0"


fake_repo_name = "SomeRepo"
fake_description = """## Fixes\n - Test fixes"""
fake_repo = FakeRepo
created_release = CreatedRelease
deleted_release = DeletedRelease
fake_release = Release
fake_tag = "v1.0.0"
fake_commit_sha = "somecommitsha"

migrate_releases = MigrateReleases()


def test_migrate_release(mocker: MockerFixture):

    get_repository_releases_mock = mocker.patch(
        "api.GithubManager.get_repository_releases", return_value=[Release]
    )
    create_new_tag_and_release_mock = mocker.patch(
        "api.GithubManager.create_new_tag_and_release", return_value=created_release
    )
    delete_release_and_tag_mock = mocker.patch(
        "api.GithubManager.delete_release_and_tag"
    )

    migrate_releases.migrate_releases(fake_repo)

    get_repository_releases_mock.assert_called_once_with(fake_repo)
    create_new_tag_and_release_mock.assert_called_once_with(
        fake_repo, fake_tag, fake_description, commit_sha=fake_commit_sha
    )
    delete_release_and_tag_mock.assert_called_once_with(fake_repo, fake_release)
    assert (
        migrate_releases.replace_tag_and_release(fake_repo, fake_release)
        == created_release
    )
