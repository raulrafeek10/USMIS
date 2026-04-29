const viewBtn =
document.getElementById("viewAllBtn");

let expanded = false;

viewBtn.addEventListener("click", function () {

const hiddenItems =
document.querySelectorAll(".hidden");

if (!expanded) {

hiddenItems.forEach(item => {

item.style.display = "flex";

});

viewBtn.innerText =
"Show less ←";

expanded = true;

}

else {

hiddenItems.forEach(item => {

item.style.display = "none";

});

viewBtn.innerText =
"View all →";

expanded = false;

}

});