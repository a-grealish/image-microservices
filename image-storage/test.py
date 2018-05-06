import unittest
import requests
import uuid

BASE_URL = "http://127.0.0.1:8080"

class TestImageUpload(unittest.TestCase):
    def setUp(self):
        self.url = BASE_URL+"/images"        

    def tearDown(self):
        pass

    def test_normal_upload(self):

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"image\"; filename=\".\\test_image.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Cache-Control': "no-cache"
        }

        r = requests.request("POST", self.url, data=payload, headers=headers)

        assert(r.status_code == 201)

    def test_bad_image_key(self):
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"bad_image_key\"; filename=\".\\test_image.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Cache-Control': "no-cache"
        }

        r = requests.request("POST", self.url, data=payload, headers=headers)

        assert(r.status_code == 400)

class TestImageDownload(unittest.TestCase):
    def setUp(self):
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"image\"; filename=\".\\test_image.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Cache-Control': "no-cache"
        }

        r = requests.request("POST", BASE_URL+'/images', data=payload, headers=headers)

        self.image_id = r.json()['image_id']

    def test_normal_download(self):
        r = requests.get(BASE_URL+'/images/'+self.image_id)

        assert(r.status_code == 200)

    def test_bad_uuid(self):
        r = requests.get(BASE_URL+'/images/not_a_uuid')

        assert(r.status_code == 400)

    def test_random_uuid(self):
        r = requests.get(BASE_URL+'/images/'+uuid.uuid4().hex)

        assert(r.status_code == 404)

class TestImageConversion(unittest.TestCase):
    def setUp(self):
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"image\"; filename=\".\\test_image.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Cache-Control': "no-cache"
        }

        r = requests.request("POST", BASE_URL+'/images', data=payload, headers=headers)

        self.image_id = r.json()['image_id']

    def test_gif_conversion(self):
        r = requests.get(BASE_URL+'/images/'+self.image_id+'.gif')

        print(r.status_code)

        assert(r.status_code == 200)


if __name__ == '__main__':
    unittest.main()
