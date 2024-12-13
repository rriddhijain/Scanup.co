import cv2
import pytesseract
from PIL import Image
import numpy as np
import os
import re

# Function to load the image from the specified path
def load_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image not found or could not be read: {image_path}")
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        raise

# Function to detect if the image has a tri-column layout
def is_tricolumn(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    # Threshold the image to create a binary image
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # Define a vertical kernel for dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    # Find contours in the dilated image
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    column_count = 0
    # Loop through contours to count potential columns
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if h > 200 and w > 20:  # Check for large rectangular regions (columns)
            column_count += 1
            # Draw rectangles around detected columns (for debugging/visualization)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the column detection result
    cv2.imshow("Column Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return column_count > 1  # Return True if more than one column is detected

# Function to binarize the image (convert it to black and white)
def binarization(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_img

# Function to separate fields on the same line based on field names
def separate_fields_on_same_line(line, field_names):
    corrected_field_names = {
        "CITY": ["CITY", "Gity"],
        "GENDER": ["GENDER", "Gender"],
        "FIRST NAME": ["FIRST NAME", "First Name"],
        "MIDDLE NAME": ["MIDDLE NAME", "Middle Name"],
        "LAST NAME": ["LAST NAME", "Last Name"],
        "DATEOFBIRTH": ["DATEOFBIRTH", "Date of Birth"],
        "STATE": ["State", "STATE"],
        "PINCODE": ["Pincode", "PINCODE"],
        "PHONE": ["Phone", "PHONE"],
        "ADDRESS LINE 1": ["ADDRESS LINE 1"],
        "ADDRESS LINE 2": ["ADDRESS LINE 2"],
        "EMAIL ADDRESS": ["EMAIL ADDRESS", "Email Address"],
    }

    # Flatten all alternative field names into a single list
    all_field_names = [alt for field in corrected_field_names.values() for alt in field]
    # Create a regex pattern to detect field names
    field_pattern = "|".join(fr"({re.escape(field)})(:?| )" for field in all_field_names)

    # Find all matches of field names in the line
    matches = list(re.finditer(field_pattern, line, re.IGNORECASE))

    # Separate fields and their values if multiple fields are on the same line
    if len(matches) > 1:
        separated_lines = []
        for i in range(len(matches)):
            field_start = matches[i].start()
            field_name = matches[i].group(1)

            if i + 1 < len(matches):
                field_end = matches[i + 1].start()
            else:
                field_end = len(line)

            field_value = line[field_start:field_end].strip()
            separated_lines.append(field_value)

        return "\n".join(separated_lines)

    return line.strip()  # Return the line unchanged if no separation is needed

# Function to preprocess OCR output text for formatting and cleanup
def preprocess_ocr_text(ocr_text):
    lines = ocr_text.split("\n")
    clean_lines = []

    # Initialize placeholders for detected fields
    first_name = None
    middle_name = None
    last_name = None
    gender_line = None
    date_of_birth = None
    city_line = None
    state_line = None
    pincode_line = None
    phone_line = None
    address_line_1 = None
    address_line_2 = None
    email_line = None

    field_names = [
        "FIRST NAME", "MIDDLE NAME", "LAST NAME", "GENDER", "DATEOFBIRTH",
        "State", "CITY", "Pincode", "Phone", "ADDRESS LINE 1", "ADDRESS LINE 2",
        "EMAIL ADDRESS"
    ]

    # Process each line to detect fields and their values
    for line in lines:
        line = line.strip()
        line = line.replace("Gity", "CITY")
        line = line.replace("=", "")
        line = separate_fields_on_same_line(line, field_names)

        # Assign fields to their respective placeholders
        if "FIRST NAME" in line:
            first_name = line
            continue
        if "MIDDLE NAME" in line:
            middle_name = line
            continue
        if "LAST NAME" in line:
            last_name = line
            continue
        if "GENDER" in line:
            gender_line = line
            continue
        if "DATEOFBIRTH" in line:
            date_of_birth = line
            continue
        if "CITY" in line:
            city_line = line
            continue
        if "State" in line:
            state_line = line
            continue
        if "Pincode" in line:
            pincode_line = line
            continue
        if "Phone" in line:
            phone_line = line
            continue
        if "ADDRESS LINE 1" in line:
            address_line_1 = line
            continue
        if "ADDRESS LINE 2" in line:
            address_line_2 = line
            continue
        if "EMAIL ADDRESS" in line:
            email_line = line
            continue

        if line:
            clean_lines.append(line)

    # Organize and format the detected fields
    ordered_lines = []
    if first_name:
        ordered_lines.append(first_name)
    if middle_name:
        ordered_lines.append(middle_name)
    if last_name:
        ordered_lines.append(last_name)

    ordered_lines.append("")

    if gender_line:
        ordered_lines.append(gender_line)
    if date_of_birth:
        ordered_lines.append(date_of_birth)
    if city_line:
        ordered_lines.append(city_line)

    ordered_lines.append("")

    if state_line:
        ordered_lines.append(state_line)
    if pincode_line:
        ordered_lines.append(pincode_line)
    if email_line:
        ordered_lines.append(email_line)
    if phone_line:
        ordered_lines.append(phone_line)
    if address_line_1:
        ordered_lines.append(address_line_1)
    if address_line_2:
        ordered_lines.append(address_line_2)

    return "\n".join(ordered_lines)

# Function to save the OCR result and display it
def save_and_display_result(result_text):
    with open("ocr_result.txt", "w") as file:
        file.write(result_text)
    print("OCR Result:")
    print(result_text)

# Function to process single-column OCR
def single_column_ocr(img):
    img = binarization(img)
    cv2.imwrite("result_images/final_preprocessed_image.png", img)
    img_pil = Image.open("result_images/final_preprocessed_image.png")
    ocr_result = pytesseract.image_to_string(img_pil)
    formatted_result = preprocess_ocr_text(ocr_result)
    save_and_display_result(formatted_result)
    print("OCR result has been processed and saved to ocr_result.txt.")

# Function to process tri-column OCR
def tricolumn_ocr(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
    results = []

    # Process each detected column
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if h > 200 and w > 20:
            roi = gray[y:y+h, x:x+w]
            ocr_result = pytesseract.image_to_string(roi, config='--psm 6')
            results.extend(ocr_result.split("\n"))

    formatted_result = preprocess_ocr_text("\n".join(results))
    save_and_display_result(formatted_result)
    print("OCR result has been processed and saved to ocr_result.txt.")

# Function to open the saved OCR result text file
def open_text_file(file_path):
    try:
        if os.name == "nt":
            os.startfile(file_path)  # Windows
        elif os.name == "posix":
            os.system(f"open {file_path}")  # macOS/Linux
    except Exception as e:
        print(f"Failed to open the file: {e}")

# Main function to handle the OCR workflow
def main(image_path):
    try:
        img = load_image(image_path)  # Load the input image
        os.makedirs("result_images", exist_ok=True)  # Ensure the output directory exists

        # Determine the layout and process accordingly
        if is_tricolumn(img):
            print("Tri-column layout detected.")
            tricolumn_ocr(img)
        else:
            print("Single column layout detected.")
            single_column_ocr(img)

        # Open the saved OCR result
        open_text_file("ocr_result.txt")
    except Exception as e:
        print(f"An error occurred: {e}")

# Entry point of the script
if __name__ == "__main__":
    image_path = "test_images/sampleform.jpg"  # Path to the input image
    main(image_path)
