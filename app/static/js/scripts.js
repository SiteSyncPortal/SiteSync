function loadProjects() {
    // Redirect to the projects page
    window.location.href = '/projects';
}
function showAddProjectForm() {
    document.getElementById('addProjectFormContainer').style.display = 'block';
}
function validateAndSubmitProjectForm() {
    const projectName = document.getElementById('project_name').value.trim();
    const location = document.getElementById('location').value.trim();
    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;
    const status = document.getElementById('status').value;

    // Condition 1: Start date should be less than end date
    if (new Date(startDate) >= new Date(endDate)) {
        alert(`Start date (${startDate}) must be earlier than the end date (${endDate}).`);
        return false;  // Prevent form submission
    }

    // Condition 2: If status is "In Progress", set end date to null
    if (status === "In Progress") {
        document.getElementById('end_date').value = "";
    }

    // Condition 3: Ensure no duplicate project name + location
    const projectTiles = document.querySelectorAll('.project-tile');
    for (let tile of projectTiles) {
        const existingProjectName = tile.querySelector('h3').textContent.trim().toLowerCase();
        const existingLocation = tile.querySelector('p').textContent.replace('Location: ', '').trim().toLowerCase();

        if (existingProjectName === projectName && existingLocation === location) {
            alert("A project with the same name and location already exists.");
            return false;  // Prevent form submission
        }
    }

    // If all conditions are met, submit the form
    document.getElementById('addProjectForm').submit();
}

function confirmDeletion(projectId) {
    if (confirm("Are you sure you want to delete this project?")) {
        deleteProject(projectId);
    }
}

function deleteProject(projectId) {
    fetch('/delete_project', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ project_id: projectId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Project deleted successfully.');
            window.location.reload();
        } else {
            alert('Failed to delete the project.');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while deleting the project.');
    });
}
