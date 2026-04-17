import re
from typing import Optional


STACKTRACE_LINE_RE = re.compile(r"(?P<file>[\w/.-]+\.(?:py|java|js|ts))[:(](?P<line>\d+)")


def extract_file_and_line(stacktrace: str) -> tuple[Optional[str], Optional[int]]:
    if not stacktrace:
        return None, None

    match = STACKTRACE_LINE_RE.search(stacktrace)
    if not match:
        return None, None

    return match.group("file"), int(match.group("line"))
