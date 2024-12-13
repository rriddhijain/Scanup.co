

function autoFillForm() {
    chrome.storage.local.get('formData', function(result) {
        if (result.formData) {
            console.log("Data fetched:", result.formData);
            const elements = document.querySelectorAll('input, select, textarea');
            elements.forEach(element => {
                const name = element.name.toLowerCase();
                if (result.formData[name]) {
                    element.value = result.formData[name];
                    console.log("Filled element:", name, "with value:", result.formData[name]);
                }
            });
        }
    });
}

autoFillForm();
