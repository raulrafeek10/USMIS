function openPopup(){

document.getElementById("popup")
.style.display="flex";

}

/* Add */

function addCourse(){

let name=
document.getElementById("courseName").value;

let count=
document.getElementById("studentCount").value;

let table=
document.querySelector("#coursesTable tbody");

let row=table.insertRow();

row.innerHTML=`

<td>${name}</td>

<td>${count}</td>

<td>

<button class="edit-btn"
onclick="editRow(this)">

Edit

</button>

<button class="delete-btn"
onclick="deleteRow(this)">

Delete

</button>

</td>

`;

document.getElementById("popup")
.style.display="none";

}

/* Edit */

function editRow(btn){

let row=btn.parentElement.parentElement;

let name=row.cells[0];
let count=row.cells[1];

name.innerHTML=
`<input value="${name.innerText}">`;

count.innerHTML=
`<input value="${count.innerText}">`;

btn.innerText="Save";

btn.onclick=function(){

name.innerText=
name.firstChild.value;

count.innerText=
count.firstChild.value;

btn.innerText="Edit";

};

}

/* Delete */

function deleteRow(btn){

btn.parentElement.parentElement.remove();

}