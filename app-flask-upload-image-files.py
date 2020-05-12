import os, json
from flask import Flask, request
from flask_cors import CORS
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app, resources={r"/ws/*": {"origins": "*"}})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def root():
    return {'server': 'OK'}


@app.route('/ws/label', methods=['POST'])
def get_labels():
    print(request.files)
    labels = []
    for file in request.files.getlist('file'):
        print(file)
        if file.filename == 'file':
            return {'msj': 'Did not attach file'}
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            # Save image file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ### Working with image to facial recognition for example
            label='TAG_IMAGE_CODE_PER_IMAGE'
            ###
            labels.append(label)
    response = {'msj': 'Label was obtained for each file', 'labels': labels}
    json_data = json.dumps(response)
    return json_data


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = False
    app.run(host='0.0.0.0', port=port, threaded=True)
