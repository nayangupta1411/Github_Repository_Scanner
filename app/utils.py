from app.constants import DEPENDENCY_FOLDERS

def print_tree(tree, indent=""):
    for item in tree:
        print(indent + "|-- " + item["path"])
        if item.get("type") == "tree" and "children" in item:
            print_tree(item["children"], indent + "    ")


def clean_tree(tree):
    cleaned = []
    for item in tree:
        name = item["path"]
        if name in DEPENDENCY_FOLDERS:
            continue
        if item.get("type") == "tree":
            item["children"] = clean_tree(item.get("children", []))

        cleaned.append(item)

    return cleaned