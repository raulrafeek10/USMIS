/* ================= FILE NAME SHOW ================= */

let fileInput =
document.querySelector("#fileInput");

let uploadText =
document.getElementById("fileName");

if(fileInput){

fileInput.addEventListener("change", function(){

if(this.files.length > 0){

uploadText.innerText =
this.files[0].name;

}

});

}



/* ================= DATE VALIDATION ================= */

let startDate =
document.querySelector("input[name='start_date']");

let dueDate =
document.querySelector("input[name='due_date']");

if(startDate && dueDate){

dueDate.addEventListener("change", function(){

if(startDate.value && dueDate.value){

if(dueDate.value < startDate.value){

alert("Due date must be after start date");

dueDate.value = "";

}

}

});

}



/* ================= CLICK UPLOAD BOX ================= */

let uploadArea =
document.querySelector(".upload-area");

if(uploadArea){

uploadArea.addEventListener("click", function(){

fileInput.click();

});

}



/* ================= FORM SUCCESS MESSAGE ================= */

document
.getElementById("assignmentForm")
.addEventListener("submit", function(){

let msg =
document.getElementById("successMsg");

if(msg){

msg.style.display = "block";

window.scrollTo({

top: 0,
behavior: "smooth"

});

setTimeout(()=>{

msg.style.display = "none";

},3000);

}

});