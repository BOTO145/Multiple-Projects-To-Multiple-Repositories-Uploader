import os
import requests
import git
import time
import google.generativeai as genai
import random

# 🔐 GitHub Credentials
GITHUB_USERNAME = "Your-username"
GITHUB_TOKEN = "your-gtihub-token"

# 🔑 Google Gemini API Key
GENAI_API_KEY = "your-gemini-api-key"
genai.configure(api_key=GENAI_API_KEY)

# 📁 Folder containing Arduino projects
BASE_FOLDER = r"projects"
IGNORE_FOLDERS = {"libraries"}  # Ignore the libraries folder


def sanitize_repo_name(name):
    """Sanitizes the repository name by removing invalid characters."""
    name = name.strip().replace("`", "").replace(" ", "-").lower()
    name = "".join(c for c in name if c.isalnum() or c in "-_")  # Allow only alphanumeric, '-', '_'
    return name


def generate_project_name(arduino_code):
    """Uses Google Gemini to generate a meaningful and unique project name"""
    prompt = f"""
    You are an expert in Arduino/ ESP32. Suggest a short, clear (5 words or fewer), and unique name for this project.

    **Project Code:**
    ```
    {arduino_code[:1000]}  # Limiting to 1000 chars
    ```

    Ensure the name is distinct and relevant. The name should resemble a GitHub repository (e.g., 'smart-door-lock', 'esp32-weather-station'). Do not repeat names.
    """

    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    response = model.generate_content(prompt)

    if response.text:
        project_name = sanitize_repo_name(response.text.strip())
    else:
        project_name = "project"  # Fallback random name

    return project_name


def generate_readme(project_path, project_name, arduino_code):
    """Generates a README.md using Google Gemini"""
    prompt = f"""
    You are an expert in Arduino/ ESP32. Generate a structured github supported aesthetic README.md file for this project.

    **Project Name:** {project_name}

    **Code:**
    ```
    {arduino_code[:1000]}
    ```

    **README Requirements:**
    - Title
    - Short description
    - Setup instructions (components, libraries)
    - Uploading and running instructions
    - Expected output
    - Troubleshooting tips
    - Took help from Chat GPT, Reddit and Arduino forums

    Format it properly using Markdown.
    """

    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    response = model.generate_content(prompt)
    readme_text = response.text if response.text else "README generation failed."

    # Save the README.md file
    with open(os.path.join(project_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_text)

    print(f"✅ README.md created for {project_name}")


def create_github_repo(project_name):
    """Creates a new GitHub repository"""
    url = "https://api.github.com/user/repos"
    data = {"name": project_name, "private": False}  # Set True for private repo

    response = requests.post(url, json=data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code == 201:
        print(f"✅ Created GitHub repo: {project_name}")
        return f"https://github.com/{GITHUB_USERNAME}/{project_name}.git"
    else:
        print(f"❌ Failed to create repo: {response.json()}")
        return None


def push_to_github(project_path, repo_url):
    """Pushes the project to GitHub, handling authentication & remote issues."""
    repo = git.Repo.init(project_path)

    # Ensure the remote URL includes authentication
    auth_repo_url = repo_url.replace("https://github.com", f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com")

    # Ensure 'origin' exists
    if "origin" in [remote.name for remote in repo.remotes]:
        origin = repo.remotes["origin"]
        origin.set_url(auth_repo_url)  # Update URL
    else:
        origin = repo.create_remote("origin", auth_repo_url)

    repo.git.add(A=True)
    repo.index.commit("Initial commit")

    # Push to GitHub with error handling
    try:
        origin.push(refspec="HEAD:main", force=True)
        print(f"🚀 Successfully pushed {project_path} to GitHub!")
    except git.exc.GitCommandError as e:
        print(f"❌ Git Push Error: {e.stderr}")



def process_projects():
    """Main function to process all Arduino projects"""
    for folder in os.listdir(BASE_FOLDER):
        project_path = os.path.join(BASE_FOLDER, folder)

        # Skip if not a folder or is in ignore list
        if not os.path.isdir(project_path) or folder in IGNORE_FOLDERS:
            continue

        # Check if Arduino code exists
        ino_files = [f for f in os.listdir(project_path) if f.endswith(".ino")]
        if not ino_files:
            print(f"⚠️ No Arduino files found in {folder}, skipping...")
            continue

        ino_file_path = os.path.join(project_path, ino_files[0])
        with open(ino_file_path, "r", encoding="utf-8") as f:
            arduino_code = f.read()

        # Step 1: Generate project name
        project_name = generate_project_name(arduino_code)
        if not project_name:
            print(f"⚠️ Failed to generate a name for {folder}, skipping...")
            continue
        print(f"🔤 AI-generated project name: `{project_name}`")

        # Step 2: Generate README.md
        generate_readme(project_path, project_name, arduino_code)

        # Step 3: Create GitHub Repository
        repo_url = create_github_repo(project_name)
        if repo_url:
            # Step 4: Push Code to GitHub
            push_to_github(project_path, repo_url)

        # Pause to avoid rate limits
        time.sleep(2)


if __name__ == "__main__":
    process_projects()
