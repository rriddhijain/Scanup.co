
function autoFillForm() {
    chrome.storage.local.get('formData', function(result) {
        if (result.formData) {
            console.log("Data fetched:", result.formData);
            const data = result.formData;

            // Define common patterns for field names
            const fieldPatterns = {
                "name": ["name","Name","firstname","Full Name","full name","full-name","full_name","fullname"],
                "first name": ["Firstname","First Name","First_Name", "First_name", "fname", "name","Name","fullname"],
                "middle name": ["middlename", "middle-name", "middle_name", "mname", "Middle Name"],
                "last name": ["lastname", "last-name", "last_name", "lname", "surname","Last Name"],
                "gender": ["gender"],
                "date of birth": ["dob", "dateofbirth", "date-of-birth", "date_of_birth"],
                "address": ["address","Address","Address Line", "address1", "address_line", "address-line", "address_line1", "address-line1"],
                "city": ["city","City","City Name","cityname"],
                "state": ["state","State","State Name","statename"],
                "pincode": ["pincode","pin code","Pincode","postalcode", "postal-code", "zip", "zipcode"],
                "contact number": ["phone", "contactnumber", "contact-number"],
                "email id": ["email", "emailaddress", "email-address"]
            };

            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    const pattern = fieldPatterns[key.toLowerCase()];
                    if (pattern) {
                        pattern.forEach(name => {
                            const element = document.getElementById(name) || document.getElementsByName(name)[0];
                            if (element) {
                                element.value = data[key];
                                console.log(`Filled element: ${name} with value: ${data[key]}`);
                            }
                        });
                    }
                }
            }
        }
    });
}

autoFillForm();
