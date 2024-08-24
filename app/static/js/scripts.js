// function loadProjects() {
//     fetch('/get_projects')
//         .then(response => response.json())
//         .then(data => {
//             let projectsDiv = document.getElementById('projects-data');
//             projectsDiv.innerHTML = ''; // Clear previous content
//             data.forEach(project => {
//                 let projectElement = document.createElement('div');
//                 projectElement.className = 'project';
//                 projectElement.innerHTML = `<h3>${project.name}</h3><p>Status: ${project.status}</p>`;
//                 projectsDiv.appendChild(projectElement);
//             });
//         })
//         .catch(error => console.error('Error fetching projects:', error));
// }
function loadProjects() {
    // Redirect to the projects page
    window.location.href = '/projects';
}
