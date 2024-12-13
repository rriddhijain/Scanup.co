from flask import Flask, request, jsonify
import os
import subprocess
import shutil
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://10.61.0.239:5500"])  # Allow only requests from localhost:5500


# Ensure the 'uploads' and 'result_images' directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('result_images', exist_ok=True)

# Path to the OCR result file
ocr_result_path = "ocr_result.txt"

# Function to process OCR with your script
def run_ocr(image_path):
    try:
        result = subprocess.run(['python', 'Final_ocr_reader.py', image_path], check=True, capture_output=True)
        print("OCR Output:", result.stdout.decode())  # Print the output of the OCR script
        return jsonify({"success": True, "file_path": ocr_result_path})
    except subprocess.CalledProcessError as e:
        print(f"Error running OCR: {e}")
        print(f"Error Output: {e.output.decode()}")  # Print the error output
        return jsonify({"success": False, "error": f"OCR processing failed: {str(e)}"}), 500



@app.route('/upload', methods=['POST'])
def upload_file():
    print("Upload request received.")  # Add this log
    if 'file' not in request.files:
        print("No file part")
        return jsonify({"success": False, "error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        print("No selected file")
        return jsonify({"success": False, "error": "No selected file"}), 400

    # Save the uploaded file as 'input_img.jpg'
    file_path = os.path.join('uploads', 'input_img.jpg')
    file.save(file_path)
    if os.path.exists(file_path):
        print(f"File saved at {file_path}")
    else:
        print("File was not saved successfully")

    # Run OCR on the uploaded file
    result = run_ocr(file_path)  # Store the result
    print(result)  # Print the result for debugging

    return result  # Return the result here directly, check if it's properly returned




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
