from flask import Flask, render_template, request, send_file
import tensorflow as tf
import numpy as np
import cv2
import os
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Load Model
MODEL_PATH = "model.h5"  # Ensure the model is correctly loaded
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model:", str(e))

UPLOAD_FOLDER = "static/uploads"
PDF_FOLDER = "static/reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)


def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Change as needed
    img = cv2.resize(img, (256, 256))  # Adjust size based on model input
    img = np.stack([img] * 3, axis=-1)
    img = np.expand_dims(img, axis=0) # Add batch dimension
    img = img.astype(np.float32) / 255.0

    print(f"Processed Image Shape: {img.shape}")
    return img


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if file is uploaded
        if "file" not in request.files:
            return "No file part", 400

        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)  # Save file

            # Process image
            img = preprocess_image(filepath)

            print(f"Final Input Shape to Model: {img.shape}")  # Debugging line

            try:
                prediction = model.predict(img)  # Get prediction
            except Exception as e:
                print(f"Model Prediction Error: {e}")  # Debugging Error
                return "Analysis failed. Try again.", 500

            # Dummy logic for classification result
            classes = ["Normal", "Pneumonia", "COVID-19", "Lung Opacity"]
            predicted_label = classes[np.argmax(prediction)]  # Get predicted class

            # Generate PDF
            pdf_path = os.path.join(PDF_FOLDER, "prediction.pdf")
            c = canvas.Canvas(pdf_path)

            c.drawString(100, 750, "Medical Report")
            c.drawString(100, 730, "------------------------------------")
            c.drawString(100, 710, f"Prediction: {predicted_label}")  # Dynamic result
            c.save()

            # Return PDF for automatic download
            return send_file(pdf_path, as_attachment=True)

    return render_template("covnet.html")


if __name__ == "__main__":
    app.run(debug=True)
