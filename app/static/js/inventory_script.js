document.addEventListener('DOMContentLoaded', function() {

    // Get project_name and location from data attributes
    const inventoryData = document.getElementById('inventory-data');
    const projectName = inventoryData.getAttribute('data-project-name');
    const location = inventoryData.getAttribute('data-location');

    // Now you can use projectName and location in your fetch function
    console.log(`Project Name: ${projectName}`);
    console.log(`Location: ${location}`);

    // Search functionality
    const searchInput = document.getElementById('inventory-search');
    searchInput.addEventListener('input', function() {
        const filter = searchInput.value.toLowerCase();
        const rows = document.querySelectorAll('#inventory-table tbody tr');

        rows.forEach(row => {
            const itemName = row.querySelector('td').textContent.toLowerCase();
            row.style.display = itemName.includes(filter) ? '' : 'none';
        });
    });

    // Handle Date Selection to fetch inventory by timestamp
    const timestampInput = document.getElementById('timestamp-date');
    timestampInput.addEventListener('change', function() {
        const selectedDate = this.value;
        fetchInventoryByDate(selectedDate);
    });

    // Function to fetch inventory by date
    function fetchInventoryByDate(date) {
        const url = `/projects/${projectName}/${location}/fetch_inventory_by_date?date=${date}`;

        fetch(url)
            .then(response => response.json())
            .then(data => updateInventoryTable(data))
            .catch(error => console.error('Error fetching data:', error));
    }

    // Function to update inventory table with fetched data
    function updateInventoryTable(data) {
        const tableBody = document.querySelector('#inventory-table tbody');
        tableBody.innerHTML = '';  // Clear the current table

        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.Item}</td>
                <td>
                    <input type="number" name="quantity[]" value="${item.Quantity}" min="0" readonly>
                    <input type="hidden" name="old_quantity[]" value="${item.Quantity}">
                    <input type="hidden" name="item_name[]" value="${item.Item}">
                </td>
                <td>
                    <button type="button" class="edit-btn">Edit</button>
                </td>
                <td>
                    <button type="button" class="delete-btn" data-item="${item.Item}" data-url="/projects/${projectName}/${location}/delete_inventory_item">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });

        // Re-apply event listeners for edit and delete buttons
        addEditButtonListeners();
        addDeleteButtonListeners();
    }

    // Add Edit Button Functionality
    function addEditButtonListeners() {
        document.querySelectorAll('.edit-btn').forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');
                const quantityInput = row.querySelector('input[name="quantity[]"]');
                quantityInput.removeAttribute('readonly');
                quantityInput.focus();
            });
        });
    }

    // Add Delete Button Functionality
    function addDeleteButtonListeners() {
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', function() {
                const itemName = this.getAttribute('data-item');
                const deleteUrl = this.getAttribute('data-url');

                if (confirm(`Are you sure you want to delete ${itemName}?`)) {
                    fetch(deleteUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ item_name: itemName })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            this.closest('tr').remove(); // Remove row from table
                        } else {
                            alert('Failed to delete the item.');
                        }
                    })
                    .catch(error => console.error('Error deleting item:', error));
                }
            });
        });
    }

    // Add New Inventory Item
    document.getElementById('add-entry').addEventListener('click', function() {
        addNewItem('inventory-entries', 'add', false);
    });

    // Function to add a new item row in the Add Inventory Form
    function addNewItem(containerId, prefix, restrictToSuggestions) {
        const container = document.getElementById(containerId);
        const newIndex = container.children.length + 1;

        const newEntry = document.createElement('div');
        newEntry.classList.add('inventory-entry', 'autocomplete');
        newEntry.innerHTML = `
            <label for="${prefix}-item-name-${newIndex}">Item:</label>
            <input type="text" id="${prefix}-item-name-${newIndex}" name="item_name[]" autocomplete="off" required>
            <div id="${prefix}-suggestions-${newIndex}" class="suggestions-dropdown"></div>
            <label for="${prefix}-quantity-${newIndex}">Quantity:</label>
            <input type="number" id="${prefix}-quantity-${newIndex}" name="quantity[]" min="1" required>
            <label for="${prefix}-date-${newIndex}">Date:</label>
            <input type="date" id="${prefix}-date-${newIndex}" name="date[]" required>
            <button type="button" class="delete-entry-btn">Delete</button>
        `;
        container.appendChild(newEntry);

        // Reapply delete button functionality for the new item
        newEntry.querySelector('.delete-entry-btn').addEventListener('click', function() {
            newEntry.remove();
        });
    }

    // Initial setup: reapply listeners after DOM is loaded
    addEditButtonListeners();
    addDeleteButtonListeners();
});
