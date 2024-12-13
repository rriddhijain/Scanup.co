
chrome.runtime.onInstalled.addListener(() => {
    console.log('Extension installed');

    // Load the data from the JSON file into chrome.storage.local
    fetch(chrome.runtime.getURL('data.json'))
        .then(response => response.json())
        .then(data => {
            chrome.storage.local.set({ formData: data }, () => {
                console.log('Data loaded into storage');
            });
        })
        .catch(error => console.error('Error loading data:', error));
});

chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
    });
});
