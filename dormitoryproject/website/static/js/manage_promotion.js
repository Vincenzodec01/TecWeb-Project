$('#modPromotion').on('click', function () {
    let id_promotion = $(this).data('id');
    $('#mod-id-promotion').val(id_promotion);
})


let rooms = []

function submit_delete() {
    $('#deletePromotionForm').submit()
}

function add_name(promotion_id, str) {
    let room_name = $('#' + str + 'promotion-room').val();
    console.log(room_name);
    rooms.push(room_name)

    let newLi = document.createElement('li');
    let newDiv = document.createElement('div')
    newLi.classList.add('list-group-item', 'd-flex', 'justify-content-between');
    newDiv.innerText = room_name;
    newDiv.ariaValueNow = room_name;
    newDiv.classList.add('d-flex', 'align-items-center');
    let el_a = document.createElement('a');
    el_a.addEventListener('click', () => delete_name(newLi, room_name))
    el_a.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16"><path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/></svg>'
    newLi.appendChild(newDiv);
    newLi.appendChild(el_a);

    $('#' + promotion_id).append(newLi);
}

function delete_name(promotion_id, room_name) {
    rooms.splice(room_name, 1);
    $(promotion_id).remove();
}

async function save_promotion(str) {
    let p_id = document.getElementById('mod-id-promotion')
    let p_name = document.getElementById(str + 'promotion-name');
    let p_discount = document.getElementById(str + 'promotion-discount');
    let p_start = document.getElementById(str + 'promotion-start');
    let p_end = document.getElementById(str + 'promotion-end');

    let data = {
        promotion_id: p_id.value,
        promotion_name: p_name.value,
        promotion_discount: p_discount.value,
        promotion_start: p_start.value,
        promotion_end: p_end.value,
        room_name: rooms
    }
    await fetch('/manage-promotion', {
        method: 'post',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
        .then((response) => {
            if (response.status === 200) {
                console.log(response)
                window.location.href = '/manage-promotion'
            }
        })
        .catch(err => console.log(err))
}