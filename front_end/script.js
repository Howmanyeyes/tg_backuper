document.getElementById('frequency').addEventListener('change', function() {
    const daysOfWeek = document.getElementById('daysOfWeek');
    if (this.value === 'specific') {
        daysOfWeek.classList.remove('hidden');
    } else {
        daysOfWeek.classList.add('hidden');
    }
});

document.getElementById('doItNow').addEventListener('click', function() {
    // Get bot API and chat ID
    const botApi = document.getElementById('botApi').value;
    const chatId = document.getElementById('chatId').value;

    // Get selected folders
    const folders = document.getElementById('folders').files;
    // Get selected time
    const time = document.getElementById('time').value;
    // Get frequency
    const frequency = document.getElementById('frequency').value;
    // Get specific days if selected
    let days = [];
    if (frequency === 'specific') {
        const dayCheckboxes = document.querySelectorAll('input[name="day"]:checked');
        dayCheckboxes.forEach((checkbox) => {
            days.push(checkbox.value);
        });
    }

    // Perform the action immediately
    // This is where you would call your back-end API
    console.log('Bot API:', botApi);
    console.log('Chat ID:', chatId);
    console.log('Folders:', folders);
    console.log('Time:', time);
    console.log('Frequency:', frequency);
    if (days.length > 0) {
        console.log('Days:', days);
    }
    alert('Action performed immediately.');
});

document.getElementById('saveSettings').addEventListener('click', function() {
    // Save settings
    const botApi = document.getElementById('botApi').value;
    const chatId = document.getElementById('chatId').value;
    // You can save these settings to local storage or send them to the back-end
    // For example, using localStorage:
    localStorage.setItem('botApi', botApi);
    localStorage.setItem('chatId', chatId);
    alert('Settings saved.');
});

document.getElementById('doItByTimetable').addEventListener('click', function() {
    // Schedule action based on timetable
    // Gather all necessary data
    const botApi = document.getElementById('botApi').value;
    const chatId = document.getElementById('chatId').value;
    const folders = document.getElementById('folders').files;
    const time = document.getElementById('time').value;
    const frequency = document.getElementById('frequency').value;
    let days = [];
    if (frequency === 'specific') {
        const dayCheckboxes = document.querySelectorAll('input[name="day"]:checked');
        dayCheckboxes.forEach((checkbox) => {
            days.push(checkbox.value);
        });
    }

    // Send data to back-end to schedule action
    console.log('Bot API:', botApi);
    console.log('Chat ID:', chatId);
    console.log('Folders:', folders);
    console.log('Time:', time);
    console.log('Frequency:', frequency);
    if (days.length > 0) {
        console.log('Days:', days);
    }
    alert('Action scheduled by timetable.');
});

// Optionally, load saved settings on page load
window.addEventListener('load', function() {
    const savedBotApi = localStorage.getItem('botApi');
    const savedChatId = localStorage.getItem('chatId');
    if (savedBotApi) {
        document.getElementById('botApi').value = savedBotApi;
    }
    if (savedChatId) {
        document.getElementById('chatId').value = savedChatId;
    }
});
document.getElementById('saveSettings').addEventListener('click', function() {
    // Gather form data
    const botApi = document.getElementById('botApi').value;
    const chatIds = document.getElementById('chatId').value.split(',').map(id => id.trim());
    const time = document.getElementById('time').value;
    const frequency = document.getElementById('frequency').value;
    let frequencyData = {
        every_day: frequency === 'everyday',
        week_days: []
    };

    if (frequency === 'specific') {
        const dayCheckboxes = document.querySelectorAll('input[name="day"]:checked');
        dayCheckboxes.forEach((checkbox) => {
            const dayIndex = getDayIndex(checkbox.value);
            frequencyData.week_days.push(dayIndex);
        });
    }

    const data = {
        API: botApi,
        chats: chatIds,
        time: new Date(`1970-01-01T${time}:00`).getTime(),
        frequency: frequencyData
    };

    // Send data to back-end
    fetch('http://localhost:9112/api/save_settings/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(result => {
        alert('Settings saved successfully.');
    })
    .catch(error => {
        console.error('Error saving settings:', error);
    });
});

// Helper function to get day index from name (1 = Monday)
function getDayIndex(dayName) {
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    return days.indexOf(dayName) + 1;
}
