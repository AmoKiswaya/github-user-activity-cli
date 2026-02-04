# GITHUB USER ACTIVITY CLI
A command-line interface (CLI) tool that uses the GitHub API to fetch and display a user’s recent GitHub activity directly in the terminal.

## Features
- Runs from the Command Line terminal.
- Accepts GitHub username as an argument.
- Fetches recent activity from GitHub user using GitHub API.
- Displays activity fetched as output in a formatted version in the terminal.
- Handles errors such as HTTP error, RUNTIME error, and URL error.

## Requirements
- Python 3.10+

## Installation
1. Clone repository
```bash

git clone git@github.com:AmoKiswaya/github-user-activity-cli.git

```

2. Install dependencies (Editable mode)
```bash

pip install -e .

```

## Usage
```bash
# Fetch events from GitHub user using github-activity command
# Replace <username> with a valid GItHub username 
github-activity <username>

# Output
AmoKiswaya starred AmoKiswaya/Task-Tracker-CLI
AmoKiswaya pushed 0 commits to AmoKiswaya/github-user-activity-cli
AmoKiswaya pushed 0 commits to AmoKiswaya/github-user-activity-cli
AmoKiswaya pushed 0 commits to AmoKiswaya/github-user-activity-cli
AmoKiswaya starred public-apis/public-apis
AmoKiswaya pushed 0 commits to AmoKiswaya/github-user-activity-cli
AmoKiswaya performed CreateEvent on AmoKiswaya/github-user-activity-cli
```
## Project Reference 
https://roadmap.sh/projects/github-user-activity 