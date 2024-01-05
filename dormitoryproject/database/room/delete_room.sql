CREATE PROCEDURE delete_room(IN _room_number CHAR(3))
BEGIN
    DELETE FROM room WHERE room_number = _room_number;
end;