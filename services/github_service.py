import re
import os
import requests
from typing import Dict, Any, Optional

GITHUB_API_BASE = "https://api.github.com"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"


class GitHubService:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")

    def parse_repo_url(self, url: str) -> tuple[Optional[str], Optional[str]]:
        patterns = [
            r"github\.com/([^/]+)/([^/]+)",
            r"github\.com/([^/]+)/([^/]+)(\.git)?",
            r"github\.com/([^/]+)/([^/]+)/(?:tree|blob)/.*",
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner = match.group(1)
                repo = match.group(2).replace(".git", "")
                return owner, repo
        return None, None

    def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        resp = requests.get(f"{GITHUB_API_BASE}/repos/{owner}/{repo}", headers=headers)
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch repo: {resp.status_code}")
        return resp.json()

    def get_languages(self, owner: str, repo: str) -> Dict[str, int]:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        resp = requests.get(f"{GITHUB_API_BASE}/repos/{owner}/{repo}/languages", headers=headers)
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch languages: {resp.status_code}")
        return resp.json()

    def get_tree(self, owner: str, repo: str, branch: str, recursive: bool = True) -> Dict[str, Any]:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{branch}?recursive={'true' if recursive else 'false'}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch tree: {resp.status_code}")
        return resp.json()

    def get_file_content(self, owner: str, repo: str, branch: str, path: str) -> str:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        url = f"{GITHUB_RAW_BASE}/{owner}/{repo}/{branch}/{path}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch file: {resp.status_code}")
        return resp.text
