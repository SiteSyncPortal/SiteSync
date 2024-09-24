let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

// Dates to be highlighted (passed from Flask)
const dates = JSON.parse(document.getElementById('calendar-data').textContent);

const dpr_data = JSON.parse(document.getElementById('calendar-green-data').textContent);

// Function to generate the calendar
function generateCalendar(month, year) {
    const firstDay = new Date(year, month).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    document.getElementById("month-year").innerHTML = monthNames[month] + " " + year;

    let calendarBody = '';
    let date = 1;

    for (let i = 0; i < 6; i++) {
        let row = '<tr>';

        for (let j = 0; j < 7; j++) {
            if (i === 0 && j < firstDay) {
                row += '<td></td>';
            } else if (date > daysInMonth) {
                break;
            } else {
                const currentDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;
                if (dates.includes(currentDate)) {
                    row += `<td class="green-date" onclick="showDprData('${currentDate}')">${date}</td>`;
                } else {
                    row += `<td onclick="showForm('${currentDate}')">${date}</td>`;
                }
                date++;
            }
        }

        row += '</tr>';
        calendarBody += row;

        if (date > daysInMonth) {
            break;
        }
    }

    document.getElementById('calendar-body').innerHTML = calendarBody;
}

// Function to handle next month
function nextMonth() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    generateCalendar(currentMonth, currentYear);
}

// Function to handle previous month
function previousMonth() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    generateCalendar(currentMonth, currentYear);
}

// Add event listeners for next/prev buttons
document.getElementById("prev").addEventListener("click", previousMonth);
document.getElementById("next").addEventListener("click", nextMonth);

// Function to display DPR data
function showDprData(date) {
    document.getElementById("selected-date").innerText = date;
    document.getElementById("dpr-table-container").style.display = "block";
    document.getElementById("white-date-form").style.display = "none";

    const dprData = dpr_data.find(d => d.Date === date);
     
    if (dprData) {
        const tableHead = document.querySelector("#dpr-table thead tr");
        const tableBody = document.querySelector("#dpr-table tbody");

        tableHead.innerHTML = "";
        tableBody.innerHTML = "";

        Object.keys(dprData).forEach(key => {
            const th = document.createElement("th");
            th.innerText = key;
            tableHead.appendChild(th);
        });

        const tr = document.createElement("tr");
        Object.values(dprData).forEach(value => {
            const td = document.createElement("td");
            td.innerText = value;
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    }
}

// Function to show the form for white dates
function showForm(date) {
    document.getElementById("white-selected-date").innerText = date;
    document.getElementById("form-selected-date").value = date;
    document.getElementById("dpr-table-container").style.display = "none";
    document.getElementById("white-date-form").style.display = "block";
}

// Generate the current month's calendar
generateCalendar(currentMonth, currentYear);
