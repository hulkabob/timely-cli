import os
import re
import requests
from termcolor import cprint
from ruamel.yaml import YAML
import questionary

BEARER_TOKEN = ''
HEADERS = {
    "Authorization": f"{BEARER_TOKEN}",
    "Version": None,
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Cookie": "", # Has to be empty
    "User-Agent": None,
    "Origin": None,
    "Referer": None,
    "Connection": None,
    "Content-Length": None,
    "Accept-Encoding": None
}

# TODO: Timezone picker
timely_dir = os.path.expanduser("~/.timely")
bearer_file = os.path.join(timely_dir, "bearer")
config_file = os.path.join(timely_dir, "config")

def init():
    # Check if ~/.timely exists, if not, create it
    if not os.path.exists(timely_dir):
        print("Creating ~/.timely directory...")
        os.makedirs(timely_dir)

    # Check if the bearer file exists
    if not os.path.exists(bearer_file):
        print("Bearer file not found.")
        token = input("Please enter your Bearer token: ")

        # Save the Bearer token to the ~/.timely/bearer file
        with open(bearer_file, "w") as f:
            f.write(token)
        print(f"Bearer token saved to {bearer_file}")

    # Read the bearer token and update HEADERS
    if os.path.exists(bearer_file):
        with open(bearer_file, "r") as f:
            BEARER_TOKEN = f.read().strip()
            HEADERS["Authorization"] = BEARER_TOKEN

    # Check if the config file exists, if not, create it
    if not os.path.exists(config_file):
        cprint("[!] Config file not found.", "green")
        with open(bearer_file, 'r') as file:
            token = file.read().replace('\n', '')
        orgs = requests.get(
            "https://api.timelyapp.com/1.1/accounts",
            headers=HEADERS,
            timeout=10
        ).json()

        org_names = [ org["name"] for org in orgs ]
        org_ids = [ org["id"] for org in orgs ]
        org_name = questionary.select("Your organisation:", choices=org_names).ask()
        org_id = org_ids[org_names.index(org_name)]
        user = requests.get(
            "https://api.timelyapp.com/1.1/{}/users/current".format(org_id),
            headers=HEADERS,
            timeout=10
        ).json()

        project_id = get_projects(org_id)
        tags, tag_ids = get_tags(org_id)

        starting_time = questionary.text(
            "Enter the default start time (HH:MM):",
            validate=validate_time).ask()

        config = {
            "user": {
                "email": user["email"],
                "id": user["id"],
                "weeklyCapacity": user["weekly_capacity"]
            },
            "org":{
                "name": org_name,
                "id": org_id
            },
            "prefs": {
                "tags": tag_ids,
                "projectId": project_id,
                "startingTime": starting_time,
            }
        }
        with open(config_file, "w") as f:
            yaml = YAML(typ='unsafe')
            yaml.default_flow_style = False
            yaml.dump(config, f)
        print(f"Config file created at {config_file}")
        return config

     # Load the YAML config file
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            yaml = YAML(typ='unsafe')
            yaml.default_flow_style = False
            config = yaml.load(f)
            return config

def validate_time(input_text):
    """Validate time format (HH:MM)."""
    return re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", input_text) is not None or "Enter time in HH:MM format"


def get_projects(org_id, plain=False):
    # TODO: Plain output implementation
    projects = requests.get(
        "https://app.timelyapp.com/{}/projects.json".format(org_id),
        headers=HEADERS,
        params={
            "version": 3,
            "totals": False,
            "offset": 0,
            "limit": 1000,
            "filter": "active"
        },
        timeout=10
    ).json()
    project_map = {}
    for project in projects:
        project_map[ f'{project["name"]}/{project["description"]}' ] = project["id"]
    selected = questionary.select("Project:", choices=list(sorted(project_map.keys()))).ask()
    cprint(f"Selected project {selected}, ID: {project_map[selected]}", "cyan")
    return project_map[selected]

def traverse_tree_interactive(node):
    """Interactively traverse a tree using questionary. I hope"""
    path = [node["name"]]  # Start with the root node
    ids = [] # Skip the root, as it's artificial

    while "children" in node and node["children"]:
        # Let the user select the next step
        cprint(" -> ".join(path), "cyan")
        #selected_name = questionary.autocomplete(
        selected_name = questionary.select(
            "Select a label:",
            choices=[child["name"] for child in node["children"]]
        ).ask()

        # Find the selected child node
        node = next(child for child in node["children"] if child["name"] == selected_name)
        path.append(node["name"])
        ids.append(str(node["id"]))

    return path, ids  # Return full path once a leaf is reached

def traverse_tree_iterative(root):
    """Iteratively traverses a tree using DFS, returning paths from root to leaves."""
    stack = [(root, [root["name"]])]  # Stack contains (node, path)

    while stack:
        node, path = stack.pop()

        if "children" in node and node["children"]:
            for child in reversed(node["children"]):  # Reverse to maintain order
                stack.append((child, path + [child["name"]]))
        else:
            yield path  # If leaf node, return path


def get_tags(org_id, plain=False):
    """Get hour tags in hirerarchical and human-readable way"""
    labels = requests.get(
        "https://api.timelyapp.com/1.1/{}/labels".format(org_id),
        headers=HEADERS,
        timeout=10
    ).json()
    tree = {
            "id": 0,
            "name": "Root", # This magic is needed to make this junk data recursion-friendly.
            "children": labels
    }
    if not plain:
        cprint("Selecting tags. You need to get down to your specific work label", "cyan")
        path, ids = traverse_tree_interactive(tree)
        cprint("Your labels/tags:", "cyan")
        cprint(" -> ".join(path), "cyan")
        cprint(" -> ".join(ids), "cyan")
    else:
        paths = list(traverse_tree_iterative(tree))
        for p in paths:
            cprint(" -> ".join(p), "cyan")
    return path, ids


