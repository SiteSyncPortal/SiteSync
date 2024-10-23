document.addEventListener('DOMContentLoaded', function () {
    // Handle form submission for fetching inventory data for the selected month
    const form = document.getElementById('track-inventory-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from reloading the page

        const selectedMonth = document.getElementById('month').value; // Get the selected month

        // Ensure a month is selected
        if (!selectedMonth) {
            alert("Please select a valid month.");
            return;
        }

        fetchInventoryByMonth(selectedMonth); // Fetch inventory for the selected month
    });

    // Function to fetch inventory data by month
    function fetchInventoryByMonth(month) {
        const projectName = "{{ project_name }}"; // Dynamically populated via Flask
        const location = "{{ location }}"; // Dynamically populated via Flask
        const url = `/projects/${projectName}/${location}/fetch_inventory_by_month?month=${month}`;

        // Send a fetch request to the server to retrieve the inventory data for the selected month
        fetch(url)
            .then(response => response.json())
            .then(data => updateInventoryTable(data)) // Call function to update the table with data
            .catch(error => console.error('Error fetching data:', error)); // Log any errors
    }

    // Function to update the inventory table with the fetched data
    function updateInventoryTable(data) {
        const tableBody = document.querySelector('#inventory-table tbody');
        tableBody.innerHTML = ''; // Clear the current table before inserting new data

        // Check if data is available, otherwise display a message
        if (data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="3">No inventory data found for the selected month.</td>';
            tableBody.appendChild(row);
        } else {
            // Populate the table with the fetched data
            data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.Item}</td>
                    <td>${item.Quantity}</td>
                    <td>${item.Date}</td>
                `;
                tableBody.appendChild(row);
            });
        }
    }
    
});
