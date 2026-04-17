class GitHubClient:
    """Local stub for GitHub inspection and PR creation."""

    def inspect_code_context(self, repo: str, branch: str, file_path: str, line_number: int) -> str:
        return (
            f"Inspected repo={repo}, branch={branch}, file={file_path}, line={line_number}. "
            "Replace this with real checkout/API logic."
        )

    def create_pull_request(self, repo: str, title: str, body: str) -> str:
        return f"https://github.com/{repo}/pull/123"
