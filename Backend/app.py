import numpy as np
import io
import tensorflow as tf

from flask import Flask, request, send_file
from inference import Inference
from flask_cors import CORS, cross_origin


# initiat the inference, doing this outside any
# function as it only run once
inference = Inference("./cnn_do.h5")

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return {"root": True}


# call this function for prediction or
# simply call the function inside this function
def predict(image):
    return inference.predict(image)


@app.route("/predict", methods=["POST"])
def get_prediction():
    if "image" in request.files:
        image = request.files["image"]

        in_memory_file = io.BytesIO()
        image.save(in_memory_file)

        try:
            tf_image = tf.io.decode_image(in_memory_file.getvalue())
        except:
            return {"success": False, "error": "Fail to treat this as an image"}

        try:
            result = predict(tf_image)
        except:
            return {"success": False, "error": "Fail to predict the image"}

        return {"success": True, "result": result}
    else:
        return {"success": False, "error": "Image is not found"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

