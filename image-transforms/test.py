import unittest
import requests

BASE_URL = "http://127.0.0.1:8080"

class TestTransformUploads(unittest.TestCase):
    def test_file_upload(self):
        files = {'image': open('test_image.jpg', 'rb')}
        r = requests.post(BASE_URL+'/transform', files=files)

        assert(r.status_code == 200)
        # ToDo check same image is returned

    def test_url_upload(self):
        data = {'url': 'http://blog.arungupta.me/wp-content/uploads/2015/04/microservices-aggregator-1024x528.png'}
        r = requests.post(BASE_URL+'/transform', data=data)

        assert(r.status_code == 200)

    def test_url_upload_no_ext(self):
        data = {'url': 'http://blog.arungupta.me/wp-content/uploads/2015/04/microservices-aggregator-1024x528.png'}
        r = requests.post(BASE_URL+'/transform', data=data)

        assert(r.status_code == 200)

    def test_image_id_upload(self):
        # Upload an image to image-storage microservice
        files = {'image': open('test_image.jpg', 'rb')}
        r = requests.post(BASE_URL+'/images', files=files)
        image_id = r.json()['image_id']

        # Call the transform microservice
        data = {'image_id': image_id}
        r = requests.post(BASE_URL+'/transform', data=data)

        assert(r.status_code == 200)

class TestTransformTypes(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

