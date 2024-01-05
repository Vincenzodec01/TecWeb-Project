let passw = document.getElementById('passwordId');
let conf_passw = document.getElementById('confirm-passwordId');
let submit = document.getElementById('submit_user')

function comparePassw() {
    submit.disabled = passw.value !== conf_passw.value;
}

passw.addEventListener('keyup', () => comparePassw());
conf_passw.addEventListener('keyup', () => comparePassw());