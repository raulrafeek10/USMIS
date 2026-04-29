/* ================= DATE ================= */

let today = new Date();

document.getElementById("dateText")
.innerText =
today.toLocaleDateString(
"en-US",
{weekday:"long",day:"numeric",month:"long"}
);



/* ================= EDIT + SAVE ================= */

document
.querySelectorAll(".edit-btn")
.forEach(button=>{

button.onclick=function(){

let row =
this.closest("tr");

let id =
row.id.replace("row-","");

let assignment =
row.querySelector(".assignment");

let midterm =
row.querySelector(".midterm");

let final =
row.querySelector(".final");

if(this.innerText.includes("Edit")){

assignment.removeAttribute("readonly");
midterm.removeAttribute("readonly");
final.removeAttribute("readonly");

this.innerText="Save";

}else{

let total =
parseInt(assignment.value||0)+
parseInt(midterm.value||0)+
parseInt(final.value||0);

row.querySelector(".total")
.innerText=total;


/* SEND TO DATABASE */

fetch("/update_grade",{

method:"POST",

headers:{
"Content-Type":
"application/x-www-form-urlencoded"
},

body:

"id="+id+
"&assignment="+assignment.value+
"&midterm="+midterm.value+
"&final="+final.value

})

.then(response=>response.text())

.then(data=>{

assignment.setAttribute("readonly",true);
midterm.setAttribute("readonly",true);
final.setAttribute("readonly",true);

button.innerText="Edit";

});

}

};

});



/* ================= SEARCH ================= */

document
.getElementById("searchInput")
.addEventListener("keyup",

function(){

let value=
this.value.toLowerCase();

let rows=
document.querySelectorAll(
"#gradesTable tbody tr"
);

rows.forEach(row=>{

let name=
row.children[0]
.innerText
.toLowerCase();

row.style.display=
name.includes(value)
? ""
: "none";

});

});



/* ================= DOWNLOAD CSV ================= */

document
.getElementById("downloadBtn")
.onclick=function(){

let table=
document.getElementById("gradesTable");

let csv=[];

for(let i=0;
i<table.rows.length;
i++){

let row=[];

for(let j=0;
j<table.rows[i].cells.length-1;
j++){

row.push(
table.rows[i]
.cells[j]
.innerText
);

}

csv.push(row.join(","));

}

let csvFile=
new Blob(
[csv.join("\n")],
{type:"text/csv"}
);

let link=
document.createElement("a");

link.download="grades.csv";

link.href=
window.URL.createObjectURL(csvFile);

link.click();

};