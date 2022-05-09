from flask import Flask,request
app = Flask(__name__)
import numpy as np
import base64
from io import BytesIO
from flask_cors import CORS, cross_origin
import json
import requests
import nsvision as nv
from PIL import Image
CORS(app)

def saveImg(image_read):
    image_read=image_read.replace("data:image/jpeg;base64,","")
    img = Image.open(BytesIO(base64.b64decode(image_read)))
    img.save(fp="predict.jpg")

Labels = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']
def predict_from_serving(image_file):
    saveImg(image_file)
    image = nv.imread('predict.JPG', resize=(244, 244), normalize=True)
    image = nv.expand_dims(image, axis=0)
    data = json.dumps({
        "instances": image.tolist()
    })
    headers = {"content-type": "application/json"}
    response = requests.post('http://localhost:8501/v1/models/model:predict', data=data, headers=headers)
    print(response.json())
    result = response.json()['predictions'][0]
    pred = np.argmax(result)
    return Labels[pred]
@app.route('/', methods=['POST'])
@cross_origin()
def predict():
    image = request.form.get('image')
    res = predict_from_serving(image)
    return res

if __name__ == '__main__':
    app.run()