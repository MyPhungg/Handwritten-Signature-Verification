// Login.htmml
function goToChooseAcc(){
    window.location.href = "./chooseAcc.html";
}
function goHome() {
    window.location.href = "./user/home.html";
}
function goForgetAcc() {
    window.location.href = "./forgetAcc.html";
}
function goForgetPass() {
    window.location.href = "./forgetPass.html";
}

// forgetAcc & Pass
function showCCCD() {
    document.getElementById("cccdForm").style.display = "block";
    document.getElementById("signatureForm").style.display = "none";
}

function showSignature() {
    document.getElementById("cccdForm").style.display = "none";
    document.getElementById("signatureForm").style.display = "block";
}

function goBack() {
    window.location.href = "./login.html";
}
function showResult() {
    document.getElementById("inputForm").style.display = "none";
    document.getElementById("signatureForm").style.display = "none";
    document.getElementById("resultForm").style.display = "block";
}

//Home.html
function goInfoUser(){
    window.location.href = "./infoUser.html";

}