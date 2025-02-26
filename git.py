import requests

TOKEN = ""

# GitHub API endpoint for user repositories
BASE_URL = "https://api.github.com/user/repos"

# Headers including the authorization token
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_all_repos():
    repos = []
    page = 1  # Start from page 1

    while True:
        # Request repositories with pagination
        response = requests.get(BASE_URL, headers=HEADERS, params={"per_page": 100, "page": page, "type": "private"})

        # Check for API errors
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.json()}")
            break

        page_repos = response.json()

        # If no more repos are returned, exit the loop
        if not page_repos:
            break

        repos.extend(page_repos)  # Add retrieved repos to the list
        page += 1  # Move to the next page

    return repos

# Fetch all repositories
all_repos = get_all_repos()

# Print repository names
for repo in all_repos:
    print(repo["name"])

# Print total number of repositories retrieved
print(f"Total repositories fetched: {len(all_repos)}")
