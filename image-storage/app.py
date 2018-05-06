from flask import Flask, request, jsonify, send_file
from flask_uploads import UploadSet, IMAGES, configure_uploads
from PIL import Image
from io import BytesIO
import uuid, os

app = Flask(__name__)

# Set maximum file upload size as 64MB
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

# Original file format data store - ToDo swap for something persistant
image_metadata = {}

app.config['UPLOADS_DEFAULT_DEST'] = './'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

@app.route("/images", methods=['POST'])
def upload_image():
    if request.method == 'POST':
        image_id = uuid.uuid4().hex

        filename = images.save(request.files['image'], name=image_id+'.')
        _, image_ext = os.path.splitext(filename)

        image_metadata[image_id] = {
            'file_ext': image_ext
        }

        return jsonify({
            "image_id": image_id,
            "filename": filename
        }), 201

@app.route("/images/<image_name>", methods=['GET'])
def single_image(image_name):

    # Get the image_id and extension for the passed name
    image_id, image_ext = os.path.splitext(image_name)

    # Check that the image_id is a valid uuid
    try:
        val = uuid.UUID(image_id, version=4)
    except ValueError:
        return jsonify({'error': 'Not a valid image_id'}), 400

    try:
        orig_image_ext = image_metadata[image_id]['file_ext']
    except KeyError:
        return jsonify({'error': 'There was a error finding the original file format'}), 500

    # if no image format specified set as the original format
    if image_ext == '':
        image_ext = orig_image_ext


    # If no file format specified or if the same as original return the file else convert first
    if image_ext == orig_image_ext:
        try:
            # TODO: Loading a file with user inputed data is unsafe
            path = './images/'+image_id+image_ext
            return send_file(path)
        except:
            return jsonify({'error': 'Image with that image_id not found'}), 404
    else:
        image = Image.open('./images/'+image_id+orig_image_ext)
        mem_file = BytesIO()
        image.save(mem_file, image_ext[1:])
        mem_file.seek(0)
        return send_file(mem_file, attachment_filename=image_id+image_ext)

@app.route("/images/healthcheck")
def healthcheck():
    return jsonify({'service': 'image-storage', 'status': 'okay'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)