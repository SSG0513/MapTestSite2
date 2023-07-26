from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import json
from git import Repo

app = Flask(__name__)

def hard_reset():
    # Empty the content of data.json
    with open('data.json', 'w') as f:
        json.dump({"type": "FeatureCollection", "features": []}, f)

    # Commit and push changes
    repo = Repo(os.getcwd())
    repo.git.pull('origin', 'main')  # Pull latest changes from remote repository
    repo.git.add('data.json')
    repo.git.commit('-m', 'Hard reset')
    repo.git.push()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'reset':
            hard_reset()
        else:
            # フォームから送信されたデータを取得
            description = request.form.get('description')
            icon = request.form.get('icon')
            coordinates = request.form.get('coordinates').split(',')
            coordinates = [float(x.strip()) for x in coordinates]
            image = request.files.get('image')
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join('static/uploads', filename))

            # データを data.json に追加
            with open('data.json', 'r+') as f:
                data = json.load(f)
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
                f.seek(0)  # ファイルの先頭に戻る
                json.dump(data, f)
                f.truncate()  # 余分な部分を削除

            # Commit and push changes
            repo = Repo(os.getcwd())
            repo.git.pull('origin', 'main')  # Pull latest changes from remote repository
            repo.git.add('data.json')
            repo.git.commit('-m', 'Add new data')
            repo.git.push()

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
