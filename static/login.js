/* ================= GSAP ================= */

gsap.registerPlugin(ScrollTrigger);



/* ================= ROLE SWITCH ================= */

const roles =
document.querySelectorAll(".role");

const roleImage =
document.getElementById("roleImage");

const roleInput =
document.getElementById("roleInput");



roles.forEach(button => {

button.addEventListener("click", () => {

roles.forEach(btn =>
btn.classList.remove("active")
);

button.classList.add("active");

let role =
button.dataset.role;



if(roleInput){

roleInput.value = role;

}



/* Change image */

if (role === "student") {

changeImage("student.png");

}

else if (role === "staff") {

changeImage("staff.png");

}

else if (role === "professor") {

changeImage("professor.png");

}

});

});



/* ================= IMAGE CHANGE ================= */

function changeImage(imageName) {

if(!roleImage) return;

gsap.killTweensOf(roleImage);

gsap.to(roleImage, {

opacity: 0,

scale: 0.8,

duration: 0.25,

onComplete: () => {

roleImage.src =
"/static/" + imageName;

gsap.to(roleImage, {

opacity: 1,

scale: 1,

duration: 0.35,

ease: "power2.out"

});

}

});

}



/* ================= TOAST AUTO HIDE ================= */

window.addEventListener("load", () => {

let toast =
document.getElementById("toastError");

if(toast){

setTimeout(() => {

toast.classList.add("toast-hide");

setTimeout(()=>{

toast.remove();

},400);

},3000);

}

});