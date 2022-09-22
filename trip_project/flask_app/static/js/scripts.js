// login controller
function openForm() {
    document.getElementById("popupForm").style.display = "block";
}
function closeForm() {
    document.getElementById("popupForm").style.display = "none";
}
// menu controller
const navShowBtn = document.querySelector('.nav-show-btn');
const navHideBtn = document.querySelector('.nav-hide-btn');
const navMenu = document.querySelector('.navbar-collapse');

navShowBtn.addEventListener('click',()=>{
    navMenu.classList.add('showNav');
})

navHideBtn.addEventListener('click',()=>{
    navMenu.classList.remove('showNav');
})

let navbarDiv = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if(document.body.scrollTop > 40 || document.documentElement.scrollTop > 40){
        navbarDiv.classList.add('navbar-cng');
    } else {
        navbarDiv.classList.remove('navbar-cng');
    }
});
