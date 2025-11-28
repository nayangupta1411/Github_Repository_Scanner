import re
from .rules import SENSITIVE_FILES, SECRET_PATTERNS

def get_all_files(repo, path=""):
    files = []
    items = repo.get_contents(path)

    for item in items:
        if item.type == "file":
            files.append(item)
        elif item.type == "dir":
            files.extend(get_all_files(repo, item.path))

    return files


def scan_repo(repo):
    issues = []
    all_files = get_all_files(repo)

    file_paths = [f.path for f in all_files]
    for sf in SENSITIVE_FILES:
        if sf in file_paths:
            issues.append(("Sensitive File Found", "High"))
    if "README.md" not in file_paths:
        issues.append(("Missing README.md", "Low"))

    if "LICENSE" not in file_paths:
        issues.append(("Missing LICENSE", "Medium"))
    for file in all_files:
        try:
            content = file.decoded_content.decode("utf-8", errors="ignore")
        except:
            continue

        for name, pattern in SECRET_PATTERNS.items():
            if re.search(pattern, content):
                issues.append((f"Exposed Secret: {name}", "High"))

    return issues
