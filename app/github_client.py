from github import Github
from dotenv import load_dotenv
import os

def get_repositories(user):
    load_dotenv()
    print("Loaded Token:", os.getenv("GITHUB_TOKEN"))
    token = os.getenv("GITHUB_TOKEN")
    client = Github(token) if token else Github()

    try:
        acc = client.get_user(user)
    except:
        acc = client.get_organization(user)

    return acc.get_repos()

def get_repo_tree(repo):
    default_branch = repo.default_branch

    git_tree = repo.get_git_tree(default_branch, recursive=True)

    tree = []  

    def add_path(path_parts, current_level):
        part = path_parts[0]
        existing = next((item for item in current_level if item["path"] == part), None)
        if not existing:
            new_item = {"path": part}
            current_level.append(new_item)
            existing = new_item

        if len(path_parts) > 1:
            existing.setdefault("type", "tree")
            existing.setdefault("children", [])
            add_path(path_parts[1:], existing["children"])
        else:
            existing["type"] = "blob"

    for item in git_tree.tree:
        parts = item.path.split("/")
        add_path(parts, tree)

    return tree