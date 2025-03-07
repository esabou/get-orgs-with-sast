## Snyk Script for Managing SAST Settings
This script interacts with the Snyk API to retrieve and update the Snyk Code (SAST) settings for multiple organizations. The script checks the current SAST settings, asks whether to update them, and provides an option to disable Snyk Code (SAST) settings for organizations where it is enabled.

## Requirements
- Python 3.6 or higher
- requests - Python library
- Snyk API Token (SNYK_TOKEN)

## Installation
1. Clone the repository
> git clone https://github.com/esabou/get-orgs-with-sast.git

2. Install dependencies
> pip install -r requirements.txt

## Setup
1. Get a Snyk API Token
2. Set Environment Variable
> export SNYK_TOKEN=your_snyk_token

## USAGE
Running the script locally
1. Ensure that you have set your SNYK_TOKEN environment variable
2. Run the script:
> python get-orgs-with-sast.py
3. Provide the Group ID when prompted
4. The script will identify all Organisations under that Group and their current SAST setting

## The script will:

- List all organizations
- Display the current **SAST settings** for each organization
- Ask if you want to disable **Snyk Code (SAST)** for organizations with SAST enabled
