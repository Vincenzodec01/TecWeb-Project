$('#modRoom').on('click', function(){
    let id_room = $(this).data('id');
    $('#mod-id-room').val(id_room);
})

function submit_delete() {
    $('#deleteRoomForm').submit()
}


function add_name() {
    let room_number = document.getElementById('room-number-input')
    let childNode = document.createElement('input')
    childNode.name = 'room-number[]'
    childNode.value = room_number.value
    $('#room-number-container').append(childNode)
}


$('#modRoomNumber').on('click', function() {
    let id_room = $(this).data('id');
    $('#mod-room-number').val(id_room)
})