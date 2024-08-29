document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            this.classList.add('active');
            document.getElementById(this.dataset.tab).classList.add('active');
        });
    
    });

    // Initialize autocomplete for Add Inventory tabs
    initializeAutocomplete('inventory-entries', false);

    // Add new inventory entry
    document.getElementById('add-entry').addEventListener('click', function() {
        addNewItem('inventory-entries', 'add', false);
    });

    // Hide suggestions dropdown when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInside = event.target.closest('.autocomplete');
        if (!isClickInside) {
            document.querySelectorAll('.suggestions-dropdown').forEach(suggestionBox => {
                suggestionBox.style.display = 'none';
            });
        }
    });
    // Enable editing of quantity fields
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const quantityInput = row.querySelector('input[name="quantity[]"]');
            quantityInput.removeAttribute('readonly');
            quantityInput.focus();
        });
    });


    // Search functionality
    const searchInput = document.getElementById('inventory-search');
    searchInput.addEventListener('input', function() {
        const filter = searchInput.value.toLowerCase();
        const rows = document.querySelectorAll('#inventory-table tbody tr');

        rows.forEach(row => {
            const itemName = row.querySelector('td').textContent.toLowerCase();
            if (itemName.includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});

function initializeAutocomplete(containerId, restrictToSuggestions) {
    const container = document.getElementById(containerId);
    const itemSuggestions = JSON.parse(document.getElementById('item-suggestions-data').textContent);

    container.querySelectorAll('.autocomplete input[type="text"]').forEach(input => {
        input.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const suggestionBox = document.getElementById(`${input.id.replace('item-name', 'suggestions')}`);
            suggestionBox.innerHTML = '';
            const suggestions = itemSuggestions.filter(item => item.startsWith(query));

            if (suggestions.length > 0) {
                suggestions.forEach(suggestion => {
                    const div = document.createElement('div');
                    div.textContent = suggestion;
                    div.classList.add('suggestion-item');
                    div.onclick = () => {
                        input.value = suggestion;
                        suggestionBox.style.display = 'none';
                        input.setAttribute('data-selected', 'true');
                    };
                    suggestionBox.appendChild(div);
                });
                suggestionBox.style.display = 'block';
                input.removeAttribute('data-selected');
            } else {
                suggestionBox.style.display = 'none';
            }
        });

        // Apply restriction only for inputs in the Sell Inventory tab
        if (restrictToSuggestions) {
            input.addEventListener('blur', function() {
                if (!this.hasAttribute('data-selected')) {
                    this.value = '';  // Clear the input if the user hasn't selected a suggestion
                }
            });
        }
    });
}

// Function to add a new item row in the form
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
    `;
    container.appendChild(newEntry);

    // Reapply the autocomplete functionality to the new item input field
    const input = newEntry.querySelector('input[type="text"]');
    input.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        const suggestionBox = document.getElementById(`${prefix}-suggestions-${newIndex}`);
        suggestionBox.innerHTML = '';
        const suggestions = JSON.parse(document.getElementById('item-suggestions-data').textContent).filter(item => item.startsWith(query));

        if (suggestions.length > 0) {
            suggestions.forEach(suggestion => {
                const div = document.createElement('div');
                div.textContent = suggestion;
                div.classList.add('suggestion-item');
                div.onclick = () => {
                    input.value = suggestion;
                    suggestionBox.style.display = 'none';
                    input.setAttribute('data-selected', 'true');
                };
                suggestionBox.appendChild(div);
            });
            suggestionBox.style.display = 'block';
            input.removeAttribute('data-selected');
        } else {
            suggestionBox.style.display = 'none';
        }
    });

    // Apply restriction only if in the Sell Inventory tab
    if (restrictToSuggestions) {
        input.addEventListener('blur', function() {
            if (!this.hasAttribute('data-selected')) {
                this.value = '';  // Clear the input if the user hasn't selected a suggestion
            }
        });
    }
}
