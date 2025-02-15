// add an event listener
document.addEventListener('DOMContentLoaded', function() {
    // get the current date and time 
    let now = new Date();

    // select the Date and Time display element
    let dateTimeDisplay = document.getElementById('dateTimeDisplay');
    let dateField = document.getElementById('date');
    let timeField = document.getElementById('time');

    if (dateTimeDisplay && dateField && timeField) {
        // format the date as DD/MM/YYYY
        let day = now.getDate().toString().padStart(2, '0');
        let month = (now.getMonth() + 1).toString().padStart(2, '0');
        let year = now.getFullYear();
        let formattedDate = `${day}/${month}/${year}`;

        // format the time as HH:MM
        let hours = now.getHours().toString().padStart(2, '0');
        let minutes = now.getMinutes().toString().padStart(2, '0');
        let formattedTime = `${hours}:${minutes}`;

        // display the date and time
        dateTimeDisplay.innerText = `Date: ${formattedDate} | Time: ${formattedTime}`;

        // set the values of hidden input fields
        dateField.value = `${year}-${month}-${day}`; // format as YYYY-MM-DD for form submission
        timeField.value = `${hours}:${minutes}`;
    } else {
        console.error('DateTimeDisplay, Date field, or Time field is not found');
    }
});