#!/usr/bin/env python3
"""
Unit and integration tests for client.py (GithubOrgClient).

Covers:
- org() (unit, patching get_json)
- _public_repos_url (unit, mocking .org property)
- public_repos (unit, patching get_json and _public_repos_url)
- has_license (parameterized unit tests)
- Integration tests for public_repos using fixtures (parameterized_class)
"""
from typing import Any, Dict, List
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
import client
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """org should call get_json with the org URL and return payload."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected
        gh = client.GithubOrgClient(org_name)
        result = gh.org()
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)

    def test_public_repos_url(self) -> None:
        """_public_repos_url should extract repos_url from the org payload."""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        with patch.object(client.GithubOrgClient, 'org', return_value=payload):
            gh = client.GithubOrgClient("google")
            self.assertEqual(gh._public_repos_url, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """public_repos should return names of repos using _public_repos_url and get_json."""
        # sample payload that get_json would return when called on repos_url
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = repos_payload

        gh = client.GithubOrgClient("google")
        with patch.object(client.GithubOrgClient, '_public_repos_url', new_callable=Mock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            repos = gh.public_repos()
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url.return_value)
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Any], license_key: str,
                         expected: bool) -> None:
        """has_license should check the license key of a repository."""
        gh = client.GithubOrgClient("org")
        self.assertEqual(gh.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures."""

    @classmethod
    def setUpClass(cls) -> None:
        """Start patching requests.get and set side_effects to return fixture payloads."""
        cls.get_patcher = patch('requests.get')
        mocked_get = cls.get_patcher.start()

        # side_effect function returns a mock whose .json() returns the right payload
        def _get(url, *args, **kwargs):
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        mocked_get.side_effect = _get

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos_integration(self) -> None:
        """public_repos should return expected repo names (integration)."""
        gh = client.GithubOrgClient(self.org_payload.get("login"))
        repos = gh.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """public_repos filtering by license should return expected apache2 repos."""
        gh = client.GithubOrgClient(self.org_payload.get("login"))
        apache2 = gh.public_repos(license_key="apache-2.0")
        self.assertEqual(apache2, self.apache2_repos)
