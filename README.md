# Arduino Project Publisher

A Python tool that automatically processes Arduino/ESP32 projects, generates meaningful names and documentation using Google's Gemini AI, and uploads them to GitHub repositories.

## Overview

This tool helps manage and publish Arduino/ESP32 projects by:
- Scanning a directory for Arduino projects
- Using Google's Gemini AI to generate appropriate project names
- Creating detailed README.md files for each project
- Creating GitHub repositories with the generated names
- Pushing the code to the newly created repositories

## Features

- Automated project naming using AI
- AI-generated comprehensive documentation
- Automatic GitHub repository creation and code publishing
- Batch processing of multiple Arduino projects

## Requirements

### Dependencies
pip install requests gitpython google-generativeai

### API Keys and Credentials
- GitHub personal access token
- Google Gemini API key

## Creating a GitHub Personal Access Token
To create a GitHub personal access token (which you need for your Arduino Project Publisher script), follow these steps:
Step 1: Navigate to Developer Settings

Log in to your GitHub account
Click on your profile picture in the top-right corner
Select "Settings" from the dropdown menu
Scroll down to find "Developer settings" in the left sidebar (or go directly to https://github.com/settings/tokens)

Step 2: Generate a New Token

Click on "Personal access tokens" and then "Tokens (classic)"
Click the "Generate new token" button (or "Generate new token (classic)")
Give your token a descriptive name in the "Note" field (e.g., "Arduino Project Publisher")

Step 3: Set Permissions
For your project, you'll need the following permissions:

Select the "repo" scope to enable full control of repositories
If you plan to create organizations or manage team membership, you might need additional scopes

Step 4: Generate and Copy Token

Scroll down and click "Generate token"
IMPORTANT: Copy your new token immediately and store it safely. GitHub will only show it once!

## Google Gemini API key:

-Go to https://ai.google.dev/

-Create a project (if you don't have one)

-Enable the Gemini API

-Create API credentials and copy your API key

-Remember to keep all API keys and tokens secure and never share them publicly!

## Setup Instructions

1. Clone this repository
2. Install the required dependencies:
pip install requests gitpython google-generativeai
3. Configure your credentials:
- Replace `GITHUB_USERNAME` and `GITHUB_TOKEN` with your GitHub credentials
- Replace `GENAI_API_KEY` with your Google Gemini API key
4. Organize your Arduino projects in the `projects` folder

## Usage

1. Place your Arduino projects in individual folders inside the `projects` directory
2. Each project folder should contain at least one `.ino` file
3. Run the script:
python main-send.py

The script will:
1. Process each project folder
2. Generate an appropriate project name
3. Create a detailed README.md file
4. Create a GitHub repository with the generated name
5. Push the project files to the new repository

## Project Structure
![Arduino Project Publisher Logo](structure/structure.jpg)

## Functions

- `sanitize_repo_name(name)`: Cleans up repository names to meet GitHub requirements
- `generate_project_name(arduino_code)`: Uses Gemini AI to generate a descriptive project name
- `generate_readme(project_path, project_name, arduino_code)`: Creates a comprehensive README.md file
- `create_github_repo(project_name)`: Sets up a new GitHub repository
- `push_to_github(project_path, repo_url)`: Pushes the project to GitHub
- `process_projects()`: Main function to process all Arduino projects

## Security Notes

⚠️ **Important**: The current code includes API keys and tokens directly in the script. For security:

1. Move credentials to environment variables or a separate configuration file
2. Add this configuration file to your `.gitignore`
3. Never commit credentials to version control

## Contributing

Feel free to submit issues or pull requests to improve the functionality of this tool.

## License

This project is open source and available under the MIT License.
