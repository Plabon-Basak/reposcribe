import os
from typing import Dict, Any, List

IMPORTANT_FILES = [
    "README.md",
    "README",
    "requirements.txt",
    "pyproject.toml",
    "Pipfile",
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "composer.json",
    "Gemfile",
    "Gemfile.lock",
    "go.mod",
    "Cargo.toml",
    "Cargo.lock",
    "manage.py",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".env.example",
    "tsconfig.json",
    "next.config.js",
    "next.config.ts",
    "vercel.json",
    "Procfile",
]

MAX_FILES_TO_ANALYZE = int(os.getenv("MAX_FILES_ANALYZE", "20"))
MAX_CHARS_PER_FILE = int(os.getenv("MAX_CHARS_PER_FILE", "20000"))
MAX_TOTAL_CHARS = int(os.getenv("MAX_TOTAL_CHARS", "200000"))


class RepositoryAnalyzer:
    def __init__(self, github_service):
        self.github_service = github_service

    def analyze(self, owner: str, repo: str, url: str = "") -> Dict[str, Any]:
        repo_info = self.github_service.get_repo_info(owner, repo)
        languages = self.github_service.get_languages(owner, repo)

        default_branch = repo_info.get("default_branch", "main")

        try:
            tree = self.github_service.get_tree(owner, repo, default_branch)
        except Exception:
            tree = {"tree": []}

        tree_items = tree.get("tree", [])

        files = []
        for item in tree_items:
            if item.get("type") == "blob":
                files.append(item.get("path", ""))

        structure = sorted(files[:100])

        important = []
        for f in files:
            if f in IMPORTANT_FILES or any(f.endswith(k) if False else f == k for k in IMPORTANT_FILES):
                important.append(f)
            elif f.lower() in [x.lower() for x in IMPORTANT_FILES]:
                important.append(f)
        important = list(dict.fromkeys(important))[:MAX_FILES_TO_ANALYZE]

        file_contents = {}
        total = 0
        for path in important:
            try:
                content = self.github_service.get_file_content(owner, repo, default_branch, path)
                if len(content) > MAX_CHARS_PER_FILE:
                    content = content[:MAX_CHARS_PER_FILE]
                file_contents[path] = content
                total += len(content)
                if total > MAX_TOTAL_CHARS:
                    break
            except Exception:
                continue

        language_list = list(languages.keys()) if languages else []
        if not language_list and repo_info.get("language"):
            language_list = [repo_info.get("language")]

        return {
            "name": repo_info.get("name"),
            "description": repo_info.get("description") or "",
            "owner": owner,
            "repo": repo,
            "url": repo_info.get("html_url") or url,
            "default_branch": default_branch,
            "language": repo_info.get("language"),
            "languages": language_list,
            "topics": repo_info.get("topics", []) or [],
            "structure": structure,
            "important_files": important,
            "file_contents": file_contents,
        }
