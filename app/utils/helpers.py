from urllib.parse import urlparse


def is_safe_local_path(target: str) -> bool:
    if not target:
        return False

    parts = urlparse(target)

    return (
        parts.scheme == ""
        and parts.netloc == ""
        and target.startswith("/")
    )