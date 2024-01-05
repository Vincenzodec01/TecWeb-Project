CREATE PROCEDURE add_clean_room(IN _id_staff INT, IN _room_number CHAR(3))
BEGIN
    INSERT INTO cleaning(cleaning_id, cleaning_date, room_number, id_staff) VALUES (0, NOW(), _room_number, _id_staff);
end;

call add_clean_room(null, '200');