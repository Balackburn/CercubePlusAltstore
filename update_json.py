import json
import re
import requests

# Fetch all releases from GitHub
def fetch_releases(repo_url):
    api_url = f"https://api.github.com/repos/{repo_url}/releases"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(api_url, headers=headers)
    return response.json()

# Update the JSON file with the fetched data
def remove_html_tags(text):
    return re.sub('<[^<]+?>', '', text)

def build_versions(releases, keyword):
    versions = []

    for release in releases:
        if keyword in release["name"]:
            version_data = {}
            version_data["version"] = re.search(r"(\d+\.\d+\.\d+)", release["tag_name"]).group(1)
            version_data["date"] = release["published_at"]

            description = release["body"]
            if keyword in description:
                description = description.split(keyword, 1)[1].strip()
            
            description = remove_html_tags(description)
            description = re.sub(r'\*{2}', '', description)
            description = re.sub(r'-', '•', description)
            description = re.sub(r'`', '"', description)

            version_data["localizedDescription"] = description
            version_data["downloadURL"] = release["assets"][0]["browser_download_url"]
            version_data["size"] = release["assets"][0]["size"]

            versions.append(version_data)

    return versions

def update_json_file(json_file, releases, keyword):
    with open(json_file, "r") as file:
        data = json.load(file)

    app = data["apps"][0]
    app["versions"] = build_versions(releases, keyword)

    # Update the size of the latest release
    latest_release = releases[0]
    if keyword in latest_release["name"]:
        app["size"] = latest_release["assets"][0]["size"]

    with open(json_file, "w") as file:
        json.dump(data, file, indent=2)
        
# Main function
def main():
    repo_url = "arichorn/YouTubeRebornPlus"
    json_file = "apps.json"
    keyword = "CercubePlusExtra"

    releases = fetch_releases(repo_url)
    update_json_file(json_file, releases, keyword)

if __name__ == "__main__":
    main()