document
.getElementById("announcementForm")
.addEventListener("submit",function(e){

e.preventDefault();

let msg=
document.getElementById("successMsg");

msg.style.display="block";

window.scrollTo({

top:0,
behavior:"smooth"

});

setTimeout(()=>{

msg.style.display="none";

},3000);

});