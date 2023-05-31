import json
import re
import requests

# Fetch the latest release information from GitHub
def fetch_latest_release(repo_url, keyword):
    api_url = f"https://api.github.com/repos/{repo_url}/releases"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(api_url, headers=headers)
    releases = response.json()

    for release in releases:
        if keyword in release["name"]:
            return release

    raise ValueError(f"No release found containing the keyword '{keyword}'.")

# Update the JSON file with the fetched data
def update_json_file(json_file, fetched_data):
    with open(json_file, "r") as file:
        data = json.load(file)

    app = data["apps"][0]
    version = re.search(r"(\d+\.\d+\.\d+)", fetched_data["tag_name"]).group(1)
    app["version"] = version
    app["versionDate"] = fetched_data["published_at"]
    app["versionDescription"] = f"{fetched_data['name']} : The changelog can be found at\n{fetched_data['html_url']}"
    app["downloadURL"] = fetched_data["assets"][0]["browser_download_url"]

    with open(json_file, "w") as file:
        json.dump(data, file, indent=2)
        
# Main function
def main():
    repo_url = "arichorn/YouTubeRebornPlus"
    json_file = "apps.json"
    keyword = "CercubePlusExtra"

    fetched_data = fetch_latest_release(repo_url, keyword)
    update_json_file(json_file, fetched_data)

if __name__ == "__main__":
    main()