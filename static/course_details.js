// ================= VIEW ALL BUTTON =================

const viewBtn = document.getElementById("viewAllBtn");

let expanded = false;

viewBtn.addEventListener("click", function () {

const items =
document.querySelectorAll(".material-item");

if (!expanded) {

items.forEach((item, index) => {

if (index >= 3) {

item.style.display = "flex";

}

});

viewBtn.innerText = "Show less ←";

expanded = true;

}

else {

items.forEach((item, index) => {

if (index >= 3) {

item.style.display = "none";

}

});

viewBtn.innerText = "View all →";

expanded = false;

}

});


// ================= BROWSE BUTTON =================

const uploadBox =
document.getElementById("uploadBox");

const fileInput =
document.getElementById("fileInput");

const browseBtn =
document.getElementById("browseBtn");

browseBtn.onclick = () => {

fileInput.click();

};


// ================= FILE SELECT =================

fileInput.addEventListener("change",
function () {

if (fileInput.files.length > 0) {

const fileName =
fileInput.files[0].name;

browseBtn.innerText =
fileName;

console.log(
"Selected:",
fileName
);

}

});


// ================= DRAG & DROP =================

uploadBox.addEventListener(
"dragover",
(e) => {

e.preventDefault();

uploadBox.style.background =
"#eef0ff";

});

uploadBox.addEventListener(
"dragleave",
() => {

uploadBox.style.background =
"white";

});

uploadBox.addEventListener(
"drop",
(e) => {

e.preventDefault();

uploadBox.style.background =
"white";

// ✅ ده أهم سطر كان ناقص

fileInput.files =
e.dataTransfer.files;

if (fileInput.files.length > 0) {

browseBtn.innerText =
fileInput.files[0].name;

alert(
"File Ready To Upload ✅"
);

}

});