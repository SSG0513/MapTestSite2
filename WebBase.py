from flask import Flask, render_template, request
import os
import json
from git import Repo

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'reset':
            hard_reset()
        else:
            description = request.form.get('description')
            icon = request.form.get('icon')
            coordinates = request.form.get('coordinates').split(',')
            coordinates = [float(x.strip()) for x in coordinates]
            # proceed with your code
            # ...

    return render_template('index.html')
def hard_reset():
    # Empty the content of data.json
    with open('data.json', 'w') as f:
        json.dump({"type": "FeatureCollection", "features": []}, f)

    # Commit and push changes
    repo = Repo(os.getcwd())
    repo.git.pull('origin', 'master')  # Pull latest changes from remote repository
    repo.git.add('data.json')
    repo.git.commit('-m', 'Hard reset')
    repo.git.push()


def main():
    action = input("Enter 'reset' to hard reset data.json, or anything else to proceed normally: ")

    if action == 'reset':
        hard_reset()
    else:
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
    app.run(debug=True)
