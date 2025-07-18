#!/usr/bin/env python3
"""Test client.GithubOrgClient class."""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(
            self,
            org_name: str,
            mock_get_json: unittest.mock.Mock,
    ) -> None:
        """Test GithubOrgClient.org returns correct value."""
        test_class = GithubOrgClient(org_name)
        test_class.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

@patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(
            self,
            mock_org: unittest.mock.Mock,
    ) -> None:
        """Test _public_repos_url property."""
        test_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_org.return_value = test_payload
        test_class = GithubOrgClient("google")
        self.assertEqual(
            test_class._public_repos_url,
            test_payload["repos_url"]
        )

@patch('client.get_json')
    def test_public_repos(
            self,
            mock_get_json: unittest.mock.Mock,
    ) -> None:
        """Test public_repos method."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://example.com/repos"
            test_class = GithubOrgClient("test")
            self.assertEqual(
                test_class.public_repos(),
                ["repo1", "repo2"]
            )
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

@parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
            self,
            repo: Dict,
            license_key: str,
            expected: bool,
    ) -> None:
        """Test has_license method."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )

#!/usr/bin/env python3
"""Integration test for client.GithubOrgClient."""
import unittest
from parameterized import parameterized_class
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class fixtures."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect for mock get."""
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    return self.json_data

            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            elif url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            else:
                return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class fixtures."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test public_repos method."""
        test_class = GithubOrgClient("google")
        self.assertEqual(test_class.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test public_repos with license filter."""
        test_class = GithubOrgClient("google")
        self.assertEqual(
            test_class.public_repos(license="apache-2.0"),
            self.apache2_repos
        )