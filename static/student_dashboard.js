// ================= SHOW ONLY 3 ROWS =================

const tableBody =
document.getElementById("examTableBody");

const rows =
tableBody.querySelectorAll("tr");

const viewAllBtn =
document.getElementById("viewAllBtn");

let expanded = false;



function showFirstThree(){

rows.forEach((row,index)=>{

if(index < 3){

row.style.display="";

}

else{

row.style.display="none";

}

});

}



// First Load

showFirstThree();



// ================= VIEW ALL =================

viewAllBtn.addEventListener("click",()=>{

expanded = !expanded;

if(expanded){

rows.forEach(row=>{

row.style.display="";

});

viewAllBtn.textContent="Show Less";

}

else{

showFirstThree();

viewAllBtn.textContent="View all →";

}

});



// ================= PROFILE MENU =================

// فتح وقفل القائمة

function toggleProfileMenu(){

let menu =
document.getElementById("profileMenu");

if(menu.style.display === "flex"){

menu.style.display = "none";

}

else{

menu.style.display = "flex";

}

}



// ================= CLOSE WHEN CLICK OUTSIDE =================

window.addEventListener("click",

function(e){

let profile =
document.querySelector(".profile-container");

let menu =
document.getElementById("profileMenu");

if(profile && !profile.contains(e.target)){

menu.style.display = "none";

}

});