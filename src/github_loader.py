import os
from github import Github
from .config import GITHUB_TOKEN


def get_repository(repo_url):

    repo_url = repo_url.rstrip("/")
    parts = repo_url.split("/")

    owner = parts[-2]
    repo_name = parts[-1].removesuffix(".git")

    full_repo_name = f"{owner}/{repo_name}"

    github_client = Github(GITHUB_TOKEN)

    repo = github_client.get_repo(full_repo_name)

    return repo


def get_all_files(repo, repo_files):

    all_files = []

    for file in repo_files:

        if file.type == "file":
            all_files.append(file.path)

        elif file.type == "dir":

            folder_contents = repo.get_contents(file.path)

            all_files.extend(
                get_all_files(repo, folder_contents)
            )

    return all_files


def read_files(repo, all_files):

    file_documents = []

    text_extensions = {
        ".py", ".java", ".js", ".jsx",
        ".ts", ".tsx", ".html", ".css",
        ".json", ".md", ".txt",
        ".xml", ".yml", ".yaml",
        ".sql", ".ipynb"
    }

    for file_path in all_files:

        extension = os.path.splitext(file_path)[1].lower()

        if extension not in text_extensions:
            print(f"Skipping: {file_path}")
            continue

        try:

            file = repo.get_contents(file_path)

            content = file.decoded_content.decode("utf-8")

            file_documents.append({
                "File Path": file_path,
                "File Content": content
            })

        except UnicodeDecodeError:
            print(f"Skipping non-UTF-8 file: {file_path}")

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return file_documents