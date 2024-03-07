from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

model = load_model('PapilledemaandPseudopapilledemaprediction.h5')

def convert_into_pixel(img):
    img = img.resize((64, 64))
    img_pixel = np.array(img)
    img_pixel = img_pixel / 255
    return img_pixel

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict')
def predict_page():
    return render_template("predict.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No selected file'})

    img = Image.open(io.BytesIO(image_file.read()))
    converted_img = convert_into_pixel(img)

    prediction = model.predict(np.expand_dims(converted_img, axis=0))
    predicted_class = np.argmax(prediction)

    if predicted_class == 0:
        result = "Normal Eye"
    elif predicted_class == 1:
        result = "Papilledema Eye"
    elif predicted_class == 2:
        result = "Pseudopapilledema Eye"

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
