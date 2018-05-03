from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
from io import BytesIO

app = Flask(__name__)

TRANSFORM = 'blur'

@app.route("/transform", methods=['POST'])
def transform_image():
    if request.method == 'POST':

        # Get the image to be transformed
        image = Image.open(request.files['image'])

        # Perform the transform
        if TRANSFORM == 'rotate':
            image = image.rotate(180)
        elif TRANSFORM == 'thumbnail':
            iamge = image.thumbnail((64, 64))
        elif TRANSFORM == 'compress':
            image = image
        elif TRANSFORM == 'blur':
            image = image.filter(ImageFilter.GaussianBlur(10))

        # Return the transformed image from memory
        mem_file = BytesIO()
        image.save(mem_file, "JPEG")
        return mem_file.getvalue(), 200, [('Content-Type', 'image/jpeg')]

@app.route("/transform/healthcheck")
def healthcheck():
    return jsonify({'service': 'image-transform', 'status': 'okay'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)