import os
from ruamel.yaml import YAML
import inquirer

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
        query = [inquirer.List(
            "org",
            message="Your Organisation:",
            choices=org_names,
        )]
        org_name = inquirer.prompt(query)["org"]
        org_id = org_ids[org_names.index(org_name)]
        user = requests.get(
            "https://api.timelyapp.com/1.1/{}/users/current".format(org_id),
            headers=HEADERS,
            timeout=10
        ).json()

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
            print("IM LOADING!")
            yaml = YAML(typ='unsafe')
            yaml.default_flow_style = False
            config = yaml.load(f)
            return config
