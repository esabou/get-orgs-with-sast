import os
import requests

# Define base URL and API version
BASE_URL = "https://api.snyk.io/rest"
API_VERSION = "2024-10-15"

# Retrieve API token from environment variable
SNYK_TOKEN = os.getenv("SNYK_TOKEN")

if not SNYK_TOKEN:
    raise ValueError("SNYK_TOKEN environment variable is not set!")


def get_group_id():
    """Prompt the user to enter a Group ID."""
    group_id = input("Enter the Group ID you want to check: ").strip()
    if not group_id:
        print("Error: Group ID cannot be empty.")
        exit(1)
    return group_id


def get_organizations(group_id):
    url = f"{BASE_URL}/groups/{group_id}/orgs?version={API_VERSION}"
    headers = {
        "Authorization": f"token {SNYK_TOKEN}",
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data", [])
        org_ids = [{"id": org["id"], "name": org["attributes"]["name"]} for org in data]
        return org_ids
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def get_sast_enabled(org_id):
    url = f"{BASE_URL}/orgs/{org_id}/settings/sast?version={API_VERSION}"
    headers = {
        "Authorization": f"token {SNYK_TOKEN}",
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data", {})
        sast_enabled = data.get("attributes", {}).get("sast_enabled", None)
        return sast_enabled
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def update_sast_setting(org_id):
    url = f"{BASE_URL}/orgs/{org_id}/settings/sast?version={API_VERSION}"
    headers = {
        "Authorization": f"token {SNYK_TOKEN}",
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }

    payload = {
        "data": {
            "id": org_id,
            "type": "sast_settings",
            "attributes": {
                "sast_enabled": False
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print(f"Snyk Code is now disabled for org_id {org_id}")
    else:
        print(f"Error: {response.status_code}, {response.text}")


def main():
    group_id = get_group_id()

    # Get all organization IDs and names
    orgs = get_organizations(group_id)

    if orgs:
        org_to_update = []  # List to store orgs with sast_enabled = True

        # Check SAST settings for each organization
        for org in orgs:
            org_id = org["id"]
            org_name = org["name"]
            print(f"Checking SAST settings for org_id: {org_id} ({org_name})")
            sast_enabled = get_sast_enabled(org_id)
            if sast_enabled is not None:
                print(f"SAST Enabled for org_id {org_id}: {sast_enabled}")
                if sast_enabled:
                    org_to_update.append(org_id)
            else:
                print(f"Failed to retrieve SAST settings for org_id {org_id}")

        # Ask if you want to update the SAST settings for organizations with sast_enabled = True
        if org_to_update:
            user_input = input(f"\nYou have {len(org_to_update)} organizations with SAST enabled. Do you want to change all of them to False? (yes/no): ").strip().lower()
            if user_input == "yes":
                for org_id in org_to_update:
                    update_sast_setting(org_id)
            else:
                print("No changes were made.")
        else:
            print("No organizations found with SAST enabled.")
    else:
        print("Failed to retrieve organizations.")


if __name__ == "__main__":
    main()
