from flask import Flask, request, jsonify, send_file
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from io import BytesIO
import uuid, os

app = Flask(__name__)

# Set maximum file upload size as 64MB
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

# Set up a connection to the db and import the models
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
db = SQLAlchemy(app)
from models import ImageMetadata

# Configure flask_uploads with an images set
app.config['UPLOADS_DEFAULT_DEST'] = './'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

@app.route("/images", methods=['POST'])
def upload_image():
    if request.method == 'POST':
        image_id = uuid.uuid4().hex

        filename = images.save(request.files['image'], name=image_id+'.')
        _, image_ext = os.path.splitext(filename)

        # Add the metadata entry to the db
        image_metadata = ImageMetadata(id=image_id, file_ext=image_ext)
        db.session.add(image_metadata)
        db.session.commit()

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

    # Load the images metadata from the db
    try:
        image_metadata = ImageMetadata.query.filter_by(id=image_id).one()
    except:
        return jsonify({'error': 'There was a error finding the image'}), 404

    # if no image format specified set as the original format
    if image_ext == '':
        image_ext = image_metadata.file_ext


    # If no file format specified or if the same as original return the file else convert first
    if image_ext == image_metadata.file_ext:
        try:
            # TODO: Loading a file with user inputed data is unsafe
            path = './images/'+image_id+image_ext
            return send_file(path)
        except:
            return jsonify({'error': 'Image with that image_id not found'}), 404
    else:
        image = Image.open('./images/'+image_id+image_metadata.file_ext)
        mem_file = BytesIO()
        image.save(mem_file, image_ext[1:])
        mem_file.seek(0)
        return send_file(mem_file, attachment_filename=image_id+image_ext)

@app.route("/images/healthcheck")
def healthcheck():
    return jsonify({'service': 'image-storage', 'status': 'okay'}), 200
