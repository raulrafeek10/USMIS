// ================= PAGE LOAD =================

document.addEventListener("DOMContentLoaded", function () {

console.log("JS Loaded ✅");


// ================= SEARCH =================

const searchInput =
document.getElementById("searchInput");

if (searchInput) {

searchInput.addEventListener("keyup", function () {

let filter =
searchInput.value.toLowerCase();

let classes =
document.querySelectorAll(".class");

classes.forEach(item => {

item.classList.remove("highlight");

if (
item.textContent
.toLowerCase()
.includes(filter)
&& filter !== ""
) {

item.classList.add("highlight");

item.scrollIntoView({
behavior: "smooth",
block: "center"
});

}

});

});

}



// ================= VIEW ALL =================

const viewBtn =
document.getElementById("viewAllBtn");

if (viewBtn) {

console.log("View Button Found ✅");

let expanded = false;

viewBtn.addEventListener("click",
function (e) {

e.preventDefault();

const extraCards =
document.querySelectorAll(".extra");

expanded = !expanded;

extraCards.forEach(card => {

card.classList.toggle("hidden");

});

viewBtn.innerHTML =
expanded
? 'Show less <i class="fa fa-arrow-left"></i>'
: 'View all <i class="fa fa-arrow-right"></i>';

});

} else {

console.log("View Button NOT Found ❌");

}



// ================= HOVER EFFECT =================

const cards =
document.querySelectorAll(".assign-card");

cards.forEach(card => {

card.addEventListener("mouseenter", () => {

card.style.transform =
"translateY(-4px)";

card.style.boxShadow =
"0 10px 20px rgba(0,0,0,0.08)";

});

card.addEventListener("mouseleave", () => {

card.style.transform =
"translateY(0)";

card.style.boxShadow =
"0 4px 10px rgba(0,0,0,0.05)";

});

});


});