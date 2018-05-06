from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
from io import BytesIO

app = Flask(__name__)

@app.route("/transform", methods=['POST'])
def transform_image():
    if request.method == 'POST':

        # Get the image to be transformed, this can be any of the following:
        # - image uploaded as a file
        # - url of a publicaly accessible image
        # - the image_id of an iamge stored in the image_storage microservice
        image = Image.open(request.files['image'])

        # Parse the query string and apply the transformation
        try:
            for key, value in request.args.items():
                if type(value) == str:
                    value = float(value)
                # Perform the transform
                if key == 'rotate':
                    image = image.rotate(value)
                elif TRANSFORM == 'thumb':
                    iamge = image.thumbnail((value, value))
                elif TRANSFORM == 'compress':
                    image = image
                elif TRANSFORM == 'blur':
                    image = image.filter(ImageFilter.GaussianBlur(value))
        except:
            return jsonify({'error': 'Could not parse filter list: {}'.format(key)}), 400

        # Return the transformed image from memory
        mem_file = BytesIO()
        image.save(mem_file, "JPEG")
        mem_file.seek(0)
        return send_file(mem_file, attachment_filename='_.jpg')

@app.route("/transform/healthcheck")
def healthcheck():
    return jsonify({'service': 'image-transform', 'status': 'okay'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)