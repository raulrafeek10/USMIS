// ================= ADD PAYMENT BUTTON =================

const addBtn =
document.querySelector(".add-btn");

if(addBtn){

addBtn.addEventListener("click", () => {

alert("Add New Payment Form Coming Soon");

});

}



// ================= METHOD OPTIONS =================

const methodIcons =
document.querySelectorAll(".method i");

methodIcons.forEach(icon => {

icon.addEventListener("click", (e) => {

e.stopPropagation();

alert("Edit / Delete Payment Method");

});

});



// ================= TABLE ROW CLICK =================

const tableRows =
document.querySelectorAll("#paymentTable tbody tr");

tableRows.forEach(row => {

row.addEventListener("click", () => {

let id =
row.querySelector("td").textContent;

alert("Payment Details Opened for " + id);

});

});



// ================= SEARCH BY ID =================

const searchInput =
document.getElementById("searchInput");

const table =
document.getElementById("paymentTable");

if(searchInput && table){

const tbody =
table.querySelector("tbody");

const rows =
tbody.querySelectorAll("tr");

searchInput.addEventListener("keyup", function () {

let filter =
searchInput.value.toUpperCase().trim();

rows.forEach(row => {

let firstCell =
row.querySelector("td");

let text =
firstCell.textContent.toUpperCase();

if (text.includes(filter)) {

row.style.display = "";

}

else {

row.style.display = "none";

}

});

});

}