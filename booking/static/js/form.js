let formValid = true;

let form = document.getElementById('submit').addEventListener('click', function (e) {
    let p1 = document.getElementById('id_password1');
    let p2 = document.getElementById('id_password2');
    if (p1.value !== p2.value) {
        alert('Passwords do not match!');
        formValid = false;
    }
    if (p1.value.length <= 8) {
        alert('Password length must be more then 8 symbols!');
        formValid = false;
    }
    if (formValid === false) {
        return false
    }
});
