from tabulate import tabulate
from app.github_client import get_repo_tree, get_repositories
from app.scanner import scan_repo
from app.utils import clean_tree, print_tree

def main():
    user = input("Enter GitHub username or organization: ")
    repos = get_repositories(user)

    if not repos:
        print("No repositories found!")
        return
    
    print("\nAvailable Repositories:")
    for i, repo in enumerate(repos, start=1):
        print(f"{i}. {repo.name}")

    
    print("\nChoose Scan Mode:")
    print("1. Scan ALL repos")
    print("2. Scan ONLY ONE repository :")
    print("3. Show structure → Remove dependencies → Show cleaned structure")
    
    mode = input("Enter choice (1 or 2 or 3): ").strip()
    

    if mode == "1":
        print("\n=== Scanning ALL Repositories ===\n")
        table = []

        for repo in repos:
            print(f"Scanning repo: {repo.name} ...")
            issues = scan_repo(repo)
            for issue, severity in issues:
                table.append([repo.name, issue, severity])

        print("\n--- Scan Report (All Repos) ---\n")
        print(tabulate(table, headers=["Repository", "Issue", "Severity"], tablefmt="grid"))
        return
    
    elif mode == "2":
        choice = int(input("\nSelect a repository (enter number): "))
        selected_repo = repos[choice - 1]
        
        print(f"\nYou selected: {selected_repo.name}")
        print("\n--- Repository Structure (Before scanning) ---\n")
        tree = get_repo_tree(selected_repo)
        print_tree(tree)
        print("\n--- Scan Report ---\n")
        issues = scan_repo(selected_repo)

        if not issues:
            print("No issues found!")
            return

        table = [[selected_repo.name, issue, severity] for issue, severity in issues]
        print(tabulate(table, headers=["Repository", "Issue", "Severity"], tablefmt="grid"))
        return
    
    elif mode == "3":
        choice = int(input("\nSelect a repository: "))
        selected_repo = repos[choice - 1]
        print(f"\nYou selected: {selected_repo.name}")
        tree = get_repo_tree(selected_repo)
        print("\n--- REPO STRUCTURE (BEFORE CLEANUP) ---\n")
        print_tree(tree)
        cleaned_tree = clean_tree(tree)
        print("\n--- REPO STRUCTURE (AFTER DEPENDENCY CLEANUP) ---\n")
        print_tree(cleaned_tree)
        return
    
    else:
        print("Invalid choice! Exiting.")
        return
 

if __name__ == "__main__":
    main()