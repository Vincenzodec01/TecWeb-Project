CREATE PROCEDURE update_room(IN _room_number CHAR(3), IN _room_type VARCHAR(20))
BEGIN
    DECLARE _id_ INT;

    SELECT id_type INTO _id_ FROM room_type WHERE name_type=_room_type;

    UPDATE room
    SET room_number = _room_number,
        id_type = IF(_id_ is null, id_type, _id_)
    WHERE room_number = _room_number;
end;