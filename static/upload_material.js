let fileInput =
document.getElementById("fileInput");

let dropArea =
document.getElementById("dropArea");

let preview =
document.getElementById("filePreview");

let fileName =
document.getElementById("fileName");

let progress =
document.getElementById("progressFill");

let cancelBtn =
document.getElementById("cancelBtn");

let selectedFile;
let interval;

/* ================= Browse ================= */

fileInput.addEventListener(
"change",
()=>{

selectedFile =
fileInput.files[0];

showPreview();

}
);

/* ================= Drag ================= */

dropArea.addEventListener(
"dragover",
(e)=>{

e.preventDefault();

dropArea.classList.add("dragover");

}
);

dropArea.addEventListener(
"dragleave",
()=>{

dropArea.classList.remove("dragover");

}
);

dropArea.addEventListener(
"drop",
(e)=>{

e.preventDefault();

dropArea.classList.remove("dragover");

selectedFile =
e.dataTransfer.files[0];

/* مهم: نحط الملف في input */

fileInput.files =
e.dataTransfer.files;

showPreview();

}
);

/* ================= Preview ================= */

function showPreview(){

if(!selectedFile) return;

fileName.innerText =
selectedFile.name;

preview.style.display="flex";

let width=0;

interval=setInterval(()=>{

if(width>=100){

clearInterval(interval);

}else{

width++;

progress.style.width=
width+"%";

}

},10);

}

/* ================= Cancel ================= */

cancelBtn.addEventListener(
"click",
()=>{

clearInterval(interval);

preview.style.display="none";

progress.style.width="0%";

fileInput.value="";

selectedFile=null;

}
);

/* ================= Date ================= */

let today=new Date();

let dateText =
document.getElementById("dateText");

if(dateText){

dateText.innerText=
today.toLocaleDateString(
"en-US",
{
weekday:"long",
day:"numeric",
month:"long"
}
);

}
