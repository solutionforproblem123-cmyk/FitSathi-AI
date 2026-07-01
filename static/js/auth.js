document.addEventListener("DOMContentLoaded", () => {

    initPasswordToggle();

    initFormValidation();

    initEmailValidation();

    initPasswordStrength();

    initConfirmPassword();

});
function initEmailValidation(){

const email=document.getElementById("email");

if(!email) return;

email.addEventListener("input",()=>{

if(validateEmail(email.value)){

email.classList.remove("error");

email.classList.add("success");

}else{

email.classList.remove("success");

email.classList.add("error");

}

});

}
function initPasswordStrength(){

const password=document.getElementById("password");

if(!password) return;

password.addEventListener("input",()=>{

const value=password.value;

password.classList.remove("weak","medium","strong");

if(value.length<6){

password.classList.add("weak");

}

else if(value.length<10){

password.classList.add("medium");

}

else{

password.classList.add("strong");

}

});

}
function initConfirmPassword(){

const password=document.getElementById("password");

const confirm=document.getElementById("confirmPassword");

if(!confirm) return;

confirm.addEventListener("input",()=>{

if(password.value===confirm.value){

confirm.classList.add("success");

confirm.classList.remove("error");

}

else{

confirm.classList.add("error");

confirm.classList.remove("success");

}

});

}
email.classList.add("error");

email.focus();

return;
email.classList.add("shake");

setTimeout(()=>{

email.classList.remove("shake");

},400);