document.addEventListener('DOMContentLoaded', function() {
    const userForm = document.getElementById('userForm');
    const userTable = document.getElementById('userTable');

    let users = [];

    userForm?.addEventListener('submit', function(event) {
        event.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;

        const user = { name, email };
        users.push(user);
        updateUserTable();
    });

    function updateUserTable() {
        userTable.innerHTML = '';
        users.forEach((user, index) => {
            const row = userTable.insertRow();
            row.insertCell(0).textContent = user.name;
            row.insertCell(1).textContent = user.email;
            const actionCell = row.insertCell(2);
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Supprimer';
            deleteButton.className = 'btn btn-danger';
            deleteButton.onclick = () => {
                users.splice(index, 1);
                updateUserTable();
            };
            actionCell.appendChild(deleteButton);
        });
    }
});
