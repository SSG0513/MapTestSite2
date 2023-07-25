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
def hard_reset():
    # Empty the content of data.json
    with open('data.json', 'w') as f:
        f.write('')

    # Commit and push changes
    repo = Repo(os.getcwd())
    repo.git.pull('origin', 'main')  # Pull latest changes from remote repository
    repo.git.add('data.json')
    repo.git.commit('-m', 'Hard reset')
    repo.git.push()

def main():
    action = input("Enter 'reset' to hard reset data.json, or anything else to proceed normally: ")

    if action == 'reset':
        hard_reset()
    else:
    in

if __name__ == "__main__":
    main()
