CREATE PROCEDURE add_room(IN _room_number CHAR(3), _type_room VARCHAR(20))
BEGIN
    DECLARE id_name INT;
    SELECT id_type INTO id_name FROM room_type WHERE name_type = _type_room;
    INSERT INTO room(room_number, id_type) VALUES (_room_number, id_name);
end;
