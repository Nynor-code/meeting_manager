document.getElementById('fetchDataBtn').addEventListener('click', fetchMeetingData);

async function fetchMeetingData() {
    const response = await fetch('/api/meetings');  // Assuming your backend has an API at this route
    const meetings = await response.json();
    displayMeetings(meetings);
}

function displayMeetings(meetings) {
    const meetingsList = document.getElementById('meetingsList');
    meetingsList.innerHTML = '';  // Clear previous meetings

    meetings.forEach(meeting => {
        const div = document.createElement('div');
        div.className = 'meetingItem';
        div.innerHTML = `<strong>${meeting.title}</strong><br>Scheduled at: ${meeting.time}`;
        meetingsList.appendChild(div);
    });
}
