import os
import json
from git import Repo

def get_input():
    # Get input from user
    description = input("Enter description: ")
    icon = input("Enter icon: ")
    while True:
        try:
            coordinates = input("Enter coordinates (comma-separated): ").split(',')
            coordinates = [float(x.strip()) for x in coordinates]
            break
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
    return description, icon, coordinates

def main():
    # Get input from user
    description, icon, coordinates = get_input()

    # Load existing data
    with open('data.json', 'r') as f:
        data = json.load(f)

    # Add new data
    new_data = {
        'type': 'Feature',
        'properties': {
            'description': description,
            'icon': icon
        },
        'geometry': {
            'type': 'Point',
            'coordinates': coordinates
        }
    }
    data['features'].append(new_data)

    # Save data
    with open('data.json', 'w') as f:
        json.dump(data, f)

    # Commit and push changes
    repo = Repo(os.getcwd())
    repo.git.pull('origin', 'main')  # Pull latest changes from remote repository
    repo.git.add('data.json')
    repo.git.commit('-m', 'Add new data')
    repo.git.push()


if __name__ == "__main__":
    main()
