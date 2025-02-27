import requests
import csv
import json

# Replace with your GitHub Personal Access Token
TOKEN = "your_github_token"

# Replace with your GitHub Organization Name
ORG_NAME = "your_org_name"

# GitHub API endpoint for fetching team access to a specific repo
TEAMS_URL_TEMPLATE = "https://api.github.com/repos/{org}/{repo}/teams"

# Headers including the authorization token
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repo_teams(repo_name):
    """Fetch teams that have access to the given repository along with their full permissions dictionary."""
    teams_url = TEAMS_URL_TEMPLATE.format(org=ORG_NAME, repo=repo_name)

    response = requests.get(teams_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error fetching teams for {repo_name}: {response.status_code} - {response.json()}")
        return []

    teams = response.json()
    
    # Extract team names and full permissions dictionary
    return [{"team_name": team["name"], "permissions": team["permissions"]} for team in teams]

def write_to_csv(repo_name, teams):
    """Write team access information for a single repository to a CSV file."""
    csv_filename = f"{repo_name}_team_permissions.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write CSV header
        writer.writerow(["Repository Name", "Team Name", "Permissions"])
        
        # Write data rows
        for team in teams:
            writer.writerow([repo_name, team["team_name"], json.dumps(team["permissions"])])
    
    print(f"CSV file generated: {csv_filename}")

def main():
    # Get user input for the repository name
    repo_name = input("Enter the repository name: ").strip()
    
    # Fetch teams with access to the given repository
    teams = get_repo_teams(repo_name)

    # Print and save results
    if teams:
        print(f"\nTeams with access to '{repo_name}':")
        for team in teams:
            print(f"Team: {team['team_name']}, Permissions: {team['permissions']}")
        
        write_to_csv(repo_name, teams)
    else:
        print(f"No team permissions found for repository '{repo_name}'.")

if __name__ == "__main__":
    main()
