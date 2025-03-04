import aiohttp
import asyncio
import json
import time

# Replace with your GitHub Personal Access Token
TOKEN = "your_github_token"

# Replace with your GitHub Organization Name
ORG_NAME = "your_org_name"

# List of repositories to process
REPO_LIST = ["repo1", "repo2", "repo3", "..."]  # Add your repos here

# GitHub API endpoints
GITHUB_API_URL = "https://api.github.com"
TEAMS_URL_TEMPLATE = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{{repo}}/teams"
BRANCHES_URL_TEMPLATE = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{{repo}}/branches"
PROTECTED_BRANCHES_URL_TEMPLATE = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{{repo}}/branches/{{branch}}/protection"
DEPLOY_KEYS_URL_TEMPLATE = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{{repo}}/keys"

# Headers including the authorization token
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# API Rate Limits
RATE_LIMIT_THRESHOLD = 50  # If remaining requests drop below this, pause
BATCH_SIZE = 50  # Number of concurrent API calls at once


async def fetch_url(session, url):
    """Generic function to make an async API request with rate limit handling."""
    async with session.get(url, headers=HEADERS) as response:
        # Handle rate limit
        remaining_requests = int(response.headers.get("X-RateLimit-Remaining", 1))
        reset_time = int(response.headers.get("X-RateLimit-Reset", time.time()))

        if remaining_requests < RATE_LIMIT_THRESHOLD:
            wait_time = reset_time - time.time()
            print(f"⚠️ Rate limit reached. Sleeping for {wait_time} seconds...")
            await asyncio.sleep(wait_time + 1)

        if response.status == 200:
            return await response.json()
        else:
            print(f"⚠️ API Error: {url} - {response.status}")
            return None


async def get_teams_access(session, repo_name):
    """Fetch teams access for a repository."""
    url = TEAMS_URL_TEMPLATE.format(repo=repo_name)
    teams = await fetch_url(session, url)
    return [{"team_name": team["name"].replace("\\", ""), "permissions": team["permissions"]} for team in teams] if teams else []


async def get_protected_branches(session, repo_name):
    """Fetch protected branches and their rules."""
    url = BRANCHES_URL_TEMPLATE.format(repo=repo_name)
    branches = await fetch_url(session, url)

    protected_branches = []
    if branches:
        for branch in branches:
            branch_name = branch["name"]
            protection_url = PROTECTED_BRANCHES_URL_TEMPLATE.format(repo=repo_name, branch=branch_name)
            protection = await fetch_url(session, protection_url)

            if protection:
                protected_branches.append({"branch_name": branch_name, "protection_rules": protection})

    return protected_branches


async def get_deploy_keys(session, repo_name):
    """Fetch deploy keys for a repository."""
    url = DEPLOY_KEYS_URL_TEMPLATE.format(repo=repo_name)
    keys = await fetch_url(session, url)
    return [{"title": key["title"], "owner": key.get("added_by", "Unknown")} for key in keys] if keys else []


async def get_repo_details(session, repo_name):
    """Fetch all details for a given repository."""
    print(f"🔄 Fetching data for repository: {repo_name}")

    teams_task = get_teams_access(session, repo_name)
    branches_task = get_protected_branches(session, repo_name)
    deploy_keys_task = get_deploy_keys(session, repo_name)

    teams_access, protected_branches, deploy_keys = await asyncio.gather(teams_task, branches_task, deploy_keys_task)

    repo_details = {
        "repo": repo_name,
        "teams_access": teams_access,
        "protected_branches": protected_branches,
        "deploy_keys": deploy_keys,
    }

    # Save JSON per repo to reduce memory load
    filename = f"{repo_name}_details.json"
    with open(filename, "w") as json_file:
        json.dump(repo_details, json_file, indent=4)

    print(f"✅ Saved: {filename}")
    return repo_details


async def process_repos():
    """Process repositories in parallel with batching."""
    async with aiohttp.ClientSession() as session:
        all_results = []
        for i in range(0, len(REPO_LIST), BATCH_SIZE):
            batch = REPO_LIST[i : i + BATCH_SIZE]
            print(f"🚀 Processing batch {i // BATCH_SIZE + 1} ({len(batch)} repos)...")
            
            tasks = [get_repo_details(session, repo) for repo in batch]
            results = await asyncio.gather(*tasks)

            # Merge results into a single JSON object
            all_results.extend(results)

        # Save all repos into a single JSON file
        with open("all_repos_details.json", "w") as json_file:
            json.dump(all_results, json_file, indent=4)
        print("✅ Saved all repos to all_repos_details.json")


def main():
    """Main function to run async processing."""
    asyncio.run(process_repos())


if __name__ == "__main__":
    main()
