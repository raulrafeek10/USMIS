document.getElementById("profLoginForm")
.addEventListener("submit", function(e){

e.preventDefault();

let email =
document.getElementById("email").value;

let password =
document.getElementById("password").value;

let error =
document.getElementById("errorMsg");

/* Example Database */

let professors = [

{
email:"prof1@sams.edu",
password:"123456"
},

{
email:"prof2@sams.edu",
password:"123456"
}

];

/* Check Login */

let validProfessor =
professors.find(user =>

user.email === email &&
user.password === password

);

if(validProfessor){

window.location.href =
"professor-dashboard.html";

}

else{

error.innerText =
"Invalid login! You are not registered as Professor.";

}

});