const apiBaseUrl = 'http://localhost:5000'; // OR 'http://localhost:8080'

// Run once on page load to populate the list
window.onload = function() {
  getAllEmployees();
};

// Fetch all employees from back-end
function getAllEmployees() {
  fetch(`${apiBaseUrl}/api/employees`)
    .then((response) => response.json())
    .then((employees) => {
      displayEmployees(employees);
    })
    .catch((error) => console.error('Error fetching employees:', error));
}

function displayEmployees(employees) {
  const listDiv = document.getElementById('employee-list');
  listDiv.innerHTML = ''; // clear previous data

  if (!employees.length) {
    listDiv.innerHTML = '<p>No employees found.</p>';
    return;
  }

  const ul = document.createElement('ul');
  employees.forEach((emp) => {
    const li = document.createElement('li');
    li.textContent = `${emp.first_name} ${emp.last_name} - ${emp.email}`;
    
    // Click to see details or edit
    li.onclick = () => {
      showEditForm(emp);
    };

    // Delete button
    const delBtn = document.createElement('button');
    delBtn.textContent = 'Delete';
    delBtn.style.marginLeft = '10px';
    delBtn.onclick = (event) => {
      event.stopPropagation(); // Prevent triggering the li.onclick
      deleteEmployee(emp.id);
    };

    li.appendChild(delBtn);
    ul.appendChild(li);
  });

  listDiv.appendChild(ul);
}

// Show create form
function showCreateForm() {
  document.getElementById('employee-id').value = '';
  document.getElementById('first-name').value = '';
  document.getElementById('last-name').value = '';
  document.getElementById('email').value = '';
  document.getElementById('department').value = '';
  document.getElementById('hire-date').value = '';
  document.getElementById('form-title').innerText = 'Create Employee';
  document.getElementById('employee-form').style.display = 'block';
}

// Show edit form
function showEditForm(emp) {
  document.getElementById('employee-id').value = emp.id;
  document.getElementById('first-name').value = emp.first_name;
  document.getElementById('last-name').value = emp.last_name;
  document.getElementById('email').value = emp.email;
  document.getElementById('department').value = emp.department || '';
  document.getElementById('hire-date').value = emp.hire_date || '';
  document.getElementById('form-title').innerText = 'Edit Employee';
  document.getElementById('employee-form').style.display = 'block';
}

// Cancel the form
function cancelForm() {
  document.getElementById('employee-form').style.display = 'none';
}

// Create or update employee
function saveEmployee(event) {
  event.preventDefault();

  const id = document.getElementById('employee-id').value;
  const first_name = document.getElementById('first-name').value;
  const last_name = document.getElementById('last-name').value;
  const email = document.getElementById('email').value;
  const department = document.getElementById('department').value;
  const hire_date = document.getElementById('hire-date').value;

  const payload = {
    first_name,
    last_name,
    email,
    department,
    hire_date
  };

  if (id) {
    // Update
    fetch(`${apiBaseUrl}/api/employees/${id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then(() => {
        cancelForm();
        getAllEmployees();
      })
      .catch((err) => console.error('Error updating employee:', err));
  } else {
    // Create
    fetch(`${apiBaseUrl}/api/employees`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then(() => {
        cancelForm();
        getAllEmployees();
      })
      .catch((err) => console.error('Error creating employee:', err));
  }
}

// Delete employee
function deleteEmployee(id) {
  fetch(`${apiBaseUrl}/api/employees/${id}`, {
    method: 'DELETE',
  })
    .then(() => {
      getAllEmployees();
    })
    .catch((err) => console.error('Error deleting employee:', err));
}
