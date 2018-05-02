from flask import Flask, request, jsonify, send_file
from flask_uploads import UploadSet, IMAGES, configure_uploads
import uuid 

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

app.config['UPLOADS_DEFAULT_DEST'] = './'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

@app.route("/")
def home():
    return "Hello World! - Image Storage"

@app.route("/images", methods=['POST'])
def upload_image():
    if request.method == 'POST':
        image_id = uuid.uuid4().hex

        filename = images.save(request.files['image'], name=image_id+'.')

        return jsonify({
            "image_id": image_id,
            "filename": filename
        }), 201

@app.route("/images/<image_name>", methods=['GET'])
def single_image(image_name):

    # ToDo: Use os extention
    image_parts = image_name.split(".")
    image_id = image_parts[0]
    if len(image_parts) == 1:
        image_ext = 'jpg'
    elif len(images) == 2:
        image_ext = image_parts[1]
    else:
        raise ValueError("Could not find a filetyep")


    return send_file('./images/'+image_id+'.jpg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)