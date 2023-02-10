function loadData() {

    fetch("http://127.0.0.1:8000/api/firstapp/first/?format=json")
        .then((response) => response.json())
        .then((data) => displayUsers(data));
}

function displayUsers(data){
    console.log(data.name)
    const ul = document.getElementById('users');
        const li = document.createElement('li');
        li.innerText = `Name:${data.name} University:${data.university}`;
        ul.appendChild(li)
}