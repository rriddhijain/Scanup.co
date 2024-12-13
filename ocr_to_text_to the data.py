import csv
import re
from translate import Translator
import json


#function to copy the contents of the text file into a csv file
def copy_txt_to_csv_english(text_file,csv_path):
    try:
        with open(text_file,"r") as f:
            text=f.read()
    except FileNotFoundError:
        print(f"Text file could not be opened at location {text_file}.\n")
        return 
    except Exception as e:
        print(f"An error occured while tring to open the file: {e}")
        return 

    first_names=[]
    middle_names=[]
    last_names=[]
    genders=[]
    dobs=[]
    addresses=[]
    cities=[]
    states=[]
    pincodes=[]
    contact_numbers=[]
    email_identity=[]
    

    #using a loop to read each line in the text
    lines=text.split('\n')
    for i,line in enumerate(lines):
        line=line.strip() 

        #using regex to check for 10 consecutive numbers 
        contact_number_match=re.findall(r'\(\d{1,3}\)-\d{3}-\d{4}|\d{10}',line)
        if contact_number_match:
            contact_numbers.extend(contact_number_match)

        #checking for pincode
        pincodes_match=re.findall(r"\b\d{6}\b",line)
        if pincodes_match:
            pincodes.extend(pincodes_match)

        #now checking for email
        email_match=re.findall(r"EMAIL ADDRESS: \s*(.+)",line)
        if email_match:
            email_identity.extend(email_match)

        #check for dobs
        dobs_match=re.findall(r'\d{2}-[01]?[0-9]-\d{4}', line)
        if dobs_match:
            dobs.extend(dobs_match)
        
        #checking for genders
        genders_match=re.findall(r"\b(male|female|others)\b",line,re.IGNORECASE)
        if genders_match:
            genders.extend(genders_match)

        #matching the city
        city_match=re.findall(r"CITY: \s*(.+)",line)
        if city_match:
            cities.extend(city_match)
        
        #matching the state
        state_match=re.findall(r"State: \s*(.+)",line)
        if state_match:
            states.extend(state_match)
        
        #matching the names:

        #1 first name
        first_name_match=re.findall(r"FIRST NAME: \s*(.+)",line)
        if first_name_match:
            first_names.extend(first_name_match)

        #middle name
        middle_name_match=re.findall(r"MIDDLE NAME: \s*(.+)",line)
        if middle_name_match:
            middle_names.extend(middle_name_match)

        #last name
        last_name_match=re.findall(r"LAST NAME: \s*(.+)",line)
        if last_name_match:
            last_names.extend(last_name_match)

        #matching address is kinda tricky as it is in 2 lines
        if "ADDRESS LINE 1:" in line:
            address_line1 = re.findall(r"ADDRESS LINE 1:\s*(.+)", line)
            address_line2 = ""
            if i + 1 < len(lines) and "ADDRESS LINE 2:" in lines[i + 1]:
                address_line2 = re.findall(r"ADDRESS LINE 2:\s*(.+)", lines[i + 1])
            
            full_address = (address_line1[0] if address_line1 else "") + " " + (address_line2[0] if address_line2 else "")
            addresses.append(full_address.strip())

    maxlen=max(
        len(first_names),len(middle_names),len(last_names),len(genders),
        len(dobs),len(addresses),len(cities),len(states),
        len(pincodes),len(contact_numbers),len(email_identity)
    )

    #writing this down in csv file
    with open(csv_path,"w",newline="") as file:
        writer=csv.writer(file)
        writer.writerow([
            "First Name","Middle Name","Last Name","Gender",
            "Date of Birth","Address",
            "City","State","Pincode","Contact Number","Email ID"])
    
        for i in range(maxlen):
            row=[
            first_names[i] if i<len(first_names) else "",
            middle_names[i] if i<len(middle_names) else "",
            last_names[i] if i<len(last_names) else "",
            genders[i] if i<len(genders) else "",
            dobs[i] if i<len(dobs) else "",
            addresses[i] if i<len(addresses) else "",
            cities[i] if i < len(cities) else "",
            states[i] if i < len(states) else "",
            pincodes[i] if i < len(pincodes) else "",
            contact_numbers[i] if i < len(contact_numbers) else "",
            email_identity[i] if i < len(email_identity) else ""
            ]
            writer.writerow(row)
    print(f"Data successfully written into {csv_path}")




#now doing it for hindi text



def safe_translate(translator, text):
    """
    Safely translate text with error handling
    """
    try:
        return translator.translate(text)
    except Exception as e:
        print(f"Translation error for text '{text}': {e}")
        return text  # Return original text if translation fails

def copy_txt_to_csv_hindi(text_file, csv_path):
    try:
        translator = Translator(from_lang="hindi", to_lang="english")
    except Exception as e:
        print(f"Translator initialization error: {e}")
        return

    try:
        with open(text_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"फ़ाइल स्थान पर नहीं मिली: {text_file}")
        return
    except Exception as e:
        print(f"फ़ाइल खोलने का प्रयास करते समय एक त्रुटि उत्पन्न हुई: {e}")
        return

    # Initialize data lists
    first_names, middle_names, last_names = [], [], []
    genders, dobs, addresses= [], [], []
    cities, states, pincodes, contact_numbers, email_identity = [], [], [], [], []

    # Reading each line in the text
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        try:
            # Contact numbers
            contact_number_match = re.findall(r'\(\d{1,3}\)-\d{3}-\d{4}|\d{10}', line)
            contact_numbers.extend(contact_number_match)

            # Pincode
            pincodes_match = re.findall(r"\b\d{6}\b", line)
            pincodes.extend(pincodes_match)

            # Email
            email_match = re.findall(r"ईमेल पता:\s*(.+)", line)
            email_identity.extend(email_match)

            # Date of Birth
            dobs_match = re.findall(r'\d{2}-[01]?[0-9]-\d{4}', line)
            dobs.extend(dobs_match)

            # Gender
            genders_match = re.findall(r"\b(पुरुष|महिला|अन्य)\b", line, re.IGNORECASE)
            genders.extend([
                "Male" if gender == "पुरुष" else 
                "Female" if gender == "महिला" else 
                "Others" for gender in genders_match
            ])

            # City
            city_match = re.findall(r"शहर:\s*(.+)", line)
            cities.extend([safe_translate(translator, city) for city in city_match])

            # State
            state_match = re.findall(r"राज्य:\s*(.+)", line)
            states.extend([safe_translate(translator, state) for state in state_match])

            # First Name
            first_name_match = re.findall(r"प्रथम नाम:\s*(.+)", line)
            first_names.extend([safe_translate(translator, name) for name in first_name_match])

            # Middle Name
            middle_name_match = re.findall(r"मध्य नाम:\s*(.+)", line)
            middle_names.extend([safe_translate(translator, name) for name in middle_name_match])

            # Last Name
            last_name_match = re.findall(r"अंतिम नाम:\s*(.+)", line)
            last_names.extend([safe_translate(translator, name) for name in last_name_match])

            # Address
            if "पता पंक्ति 1:" in line:
                address_line1 = re.findall(r"पता पंक्ति 1:\s*(.+)", line)
                address_line2 = ""
            if i + 1 < len(lines) and "पता पंक्ति 2:" in lines[i + 1]:
                address_line2 = re.findall(r"पता पंक्ति 2:\s*(.+)", lines[i + 1])
            
            full_address = (address_line1[0] if address_line1 else "") + " " + (address_line2[0] if address_line2 else "")
            addresses.append(safe_translate(translator, full_address.strip()))

        except Exception as e:
            print(f"Error processing line {i+1}: {line}")
            print(f"Specific error: {e}")
            continue

    # Calculate max length for rows
    maxlen = max(
        len(first_names), len(middle_names), len(last_names), len(genders),
        len(dobs), len(addresses), len(cities), len(states),
        len(pincodes), len(contact_numbers), len(email_identity)
    )

    # Write to CSV
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "First Name", "Middle Name", "Last Name", "Gender",
                "Date of Birth", "Address",
                "City", "State", "Pincode", "Contact Number", "Email ID"
            ])

            for i in range(maxlen):
                row = [
                    first_names[i] if i < len(first_names) else "",
                    middle_names[i] if i < len(middle_names) else "",
                    last_names[i] if i < len(last_names) else "",
                    genders[i] if i < len(genders) else "",
                    dobs[i] if i < len(dobs) else "",
                    addresses[i] if i < len(addresses) else "",
                    cities[i] if i < len(cities) else "",
                    states[i] if i < len(states) else "",
                    pincodes[i] if i < len(pincodes) else "",
                    contact_numbers[i] if i < len(contact_numbers) else "",
                    email_identity[i] if i < len(email_identity) else ""
                ]
                writer.writerow(row)

        print(f"डेटा सफलतापूर्वक {csv_path} में लिखा गया")
    except Exception as e:
        print(f"CSV में लिखने के दौरान एक त्रुटि उत्पन्न हुई: {e}")

def detect_language(text_file, csv_path):
    try:
        with open(text_file, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Detailed language detection
        hindi_chars = re.findall(r'[\u0900-\u097F]', text)
        english_chars = re.findall(r'[a-zA-Z]', text)

        print(f"Hindi characters found: {len(hindi_chars)}")
        print(f"English characters found: {len(english_chars)}")

        if len(hindi_chars) > len(english_chars):
            copy_txt_to_csv_hindi(text_file, csv_path)
        else:
            copy_txt_to_csv_english(text_file,csv_path)
    except FileNotFoundError:
        print(f"File not found at location: {text_file}")
    except UnicodeDecodeError:
        print("Error decoding the file. Please ensure the file is encoded in UTF-8.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()


# Update these paths accordingly
text_file = r"D:\divyam_folders_mosip\OCR_Result.txt"
csv_path = r"D:\divyam_folders_mosip\Output.csv"
detect_language(text_file, csv_path)
json_path=r"D:\divyam_folders_mosip\Json_Path.json"
with open(csv_path,mode="r",encoding="utf=8") as f:
    csv_reader=csv.DictReader(f)
    data=[row for row in csv_reader]
with open(json_path,mode="w",encoding="utf-8") as f:
    json.dump(data,f,indent=4,ensure_ascii=False)