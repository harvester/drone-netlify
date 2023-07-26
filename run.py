import requests
import time
import os

from github import Github

# netlify information
NETLIFY_AUTH_TOKEN = os.getenv("NETLIFY_AUTH_TOKEN")
NETLIFY_SITE_ID = os.getenv("NETLIFY_SITE_ID")

# GitHub information
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("DRONE_REPO")
GITHUB_PULL_REQUEST_ID = os.getenv("DRONE_PULL_REQUEST")
GITHUB_COMMIT = os.getenv("DRONE_COMMIT")

BUILD_ZIP_FILE = os.getenv("BUILD_ZIP_FILE", "build.zip")


# deploy BUILD_ZIP_FILE to netlify
def deploy_to_netlify():
    print("Starting the deployment...")
    headers = {
        "Content-Type": "application/zip",
        "Authorization": f"Bearer {NETLIFY_AUTH_TOKEN}"
    }

    with open(BUILD_ZIP_FILE, "rb") as zip_file:
        response = requests.post(
            f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys",
            headers=headers,
            data=zip_file
        )

    if response.status_code == 200:
        print("Deployment successful!")
        return response.json()
    else:
        print("Deployment failed with status code:", response.status_code)
        return None


# watch the deploy state until it is ready
def watch_deploy_to_ready(deploy_id):
    timeout = 300
    interval = 5
    start_time = time.time()

    print("Watching the deploy state...")
    while time.time() - start_time < timeout:
        url = f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys/{deploy_id}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data["state"] == "ready":
                print("The deploy is ready!")
                return True
        except requests.Timeout:
            print("Request timeout while watching the deploy state.")
            return False

        time.sleep(interval)
    else:
        print("Deployment timeout.")
        return False


# update or create a comment on the GitHub pull request
def update_or_create_comment(pull, deploy):
    comment_content = f"""### <span aria-hidden="true">✅</span> Deploy Preview for *{deploy["name"]}* ready!
|  Name | Link |
|:-:|------------------------|
|<span aria-hidden="true">🔨</span> Latest commit | {GITHUB_COMMIT} |
|<span aria-hidden="true">🔍</span> Latest deploy log | {deploy["admin_url"]}/deploys/{deploy["id"]} |
|<span aria-hidden="true">😎</span> Deploy Preview | [{deploy["deploy_ssl_url"]}]({deploy["deploy_ssl_url"]}) |
---
"""
    for comment in pull.get_issue_comments():
        if "Deploy Preview" in comment.body:
            print("Updating the pull request comment")
            comment.edit(comment_content)
            return

    print("Creating a new pull request comment")
    pull.create_issue_comment(comment_content)


def main():
    # deploy to Netlify and get the deploy object
    deploy = deploy_to_netlify()
    if not deploy:
        return

    # watch the deploy state until it is ready
    if not watch_deploy_to_ready(deploy["id"]):
        return

    # authenticate with GitHub API and get the pull request
    gh_api = Github(GITHUB_TOKEN)
    repo = gh_api.get_repo(GITHUB_REPO)
    pull = repo.get_pull(int(GITHUB_PULL_REQUEST_ID))

    # update or create a comment on the GitHub pull request
    update_or_create_comment(pull, deploy)

    print("Done!")


if __name__ == "__main__":
    main()
