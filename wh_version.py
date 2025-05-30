# Wahoo! Results - https://github.com/JohnStrunk/wahoo-results
# Copyright (C) 2020 - John D. Strunk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Version information."""

import datetime
import re
from typing import Any

import requests
import semver.version


class ReleaseInfo:
    """ReleaseInfo describes a single release from a GitHub repository."""

    tag: str  # The git tag of the release
    url: str  # The url to the release page
    draft: bool  # Whether the release is a draft
    prerelease: bool  # Whether the release is a prerelease
    published: datetime.datetime  # When the release was published
    semver: str  # The version corresponding to the tag

    def __init__(self, release_json: dict[str, Any]):
        """Construct a ReleaseInfo object from a JSON dictionary.

        :param release_json: The JSON dictionary from the GitHub API
        """
        self.tag = release_json["tag_name"]
        self.url = release_json["html_url"]
        self.draft = release_json["draft"]
        self.prerelease = release_json["prerelease"]
        self.published = datetime.datetime.fromisoformat(release_json["published_at"])
        match = re.match(r"^v?(.*)$", self.tag)
        self.semver = ""
        if match is not None:
            self.semver = match.group(1)


def releases(user_repo: str) -> list[ReleaseInfo]:
    """Retrieve the list of releases for the provided repo.

    user_repo should be of the form "user/repo" (i.e.,
    "JohnStrunk/wahoo-results")

    :param user_repo: The GitHub user/repo to retrieve releases from
    :returns: A list of ReleaseInfo objects
    """
    url = f"https://api.github.com/repos/{user_repo}/releases"
    # The timeout may be too fast, but it's going to hold up displaying the
    # settings screen. Better to miss an update than hang for too long.
    resp = requests.get(
        url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=2
    )
    if not resp.ok:
        return []

    body = resp.json()
    return list(map(ReleaseInfo, body))


def highest_semver(rlist: list[ReleaseInfo]) -> ReleaseInfo:
    """Take a list of releases and return the one with the highest semantic version tag.

    Assumes the tag is the semver string with an optional leading "v" (e.g.,
    "1.2" or "v1.2")

    >>> rdict = {
    ...     "html_url": "",
    ...     "draft": False,
    ...     "prerelease": False,
    ...     "published_at": "2020-01-01 00:00:00",
    ... }
    >>> v1 = ReleaseInfo(rdict | {"tag_name": "v1.0.0"})
    >>> v2 = ReleaseInfo(rdict | {"tag_name": "v2.0.0"})
    >>> v3 = ReleaseInfo(rdict | {"tag_name": "v3.0.0"})
    >>> highest_semver([v1, v2, v3]).semver
    '3.0.0'
    >>> highest_semver([v2, v3, v1]).semver
    '3.0.0'
    >>> highest_semver([v3, v1, v2]).semver
    '3.0.0'
    """
    highest = rlist[0]
    for release in rlist:
        sv_release = semver.version.Version.parse(release.semver)
        if sv_release.compare(highest.semver) > 0 and not release.prerelease:
            highest = release
    return highest


def git_semver(wrv: str) -> str:
    """Return a legal semver description of the Wahoo Results version identifier.

    :param wrv: The wahoo-results version string
    :returns: A semver string

    Git describe should be converted:
    >>> git_semver("v0.3.2-2-g97e7a82")
    '0.3.3-dev.2+97e7a82'

    Don't bump patch if it's a pre-release
    >>> git_semver("v1.2.3-pre4-5-gbadbeef")
    '1.2.3-pre4.dev.5+badbeef'
    """
    # groups: tag (w/o v), commits, hash (w/ g)
    components = re.match(r"^v?(.+)-(\d+)-g([0-9a-f]+)$", wrv)
    if components is None:
        return "0.0.1"
    version = components.group(1)
    commits = int(components.group(2))
    sha = components.group(3)
    if not semver.version.Version.is_valid(version):
        return "0.0.1"
    version_info = semver.version.Version.parse(version)
    if commits > 0:  # it's a dev version, so modify the version information
        pre = ""
        if version_info.prerelease is not None:
            pre += version_info.prerelease + "."
        else:
            version_info = version_info.bump_patch()
        pre += f"dev.{commits}"
        version_info = version_info.replace(prerelease=pre, build=sha)
    return str(version_info)


def latest() -> ReleaseInfo | None:
    """Retrieve the latest release info."""
    rlist = releases("JohnStrunk/wahoo-results")
    if len(rlist) == 0:
        return None
    return highest_semver(rlist)


def is_latest_version(latest_version: ReleaseInfo | None, wrv: str) -> bool:
    """Return true if the running version is the most recent.

    >>> rdict = {
    ...     "html_url": "",
    ...     "draft": False,
    ...     "prerelease": False,
    ...     "published_at": "2020-01-01 00:00:00",
    ... }
    >>> is_latest_version(ReleaseInfo(rdict | {"tag_name": "v1.0.0"}), "0.9.0")
    False
    >>> is_latest_version(ReleaseInfo(rdict | {"tag_name": "v1.0.0"}), "1.9.0")
    True
    >>> is_latest_version(ReleaseInfo(rdict | {"tag_name": "v1.0.0-pre1"}), "1.0.0")
    True
    """
    if latest_version is None:
        return True
    if wrv == "unreleased":
        return False
    return semver.version.Version.parse(latest_version.semver).compare(wrv) <= 0


def _main():
    release_list = releases("JohnStrunk/wahoo-results")
    for release in release_list:
        print(
            f"Release: {release.tag}, Version: {release.semver}, Published: {release.published}"
        )


if __name__ == "__main__":
    _main()
