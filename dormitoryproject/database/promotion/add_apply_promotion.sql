CREATE PROCEDURE add_promotion_room(IN p_id INT, IN p_room VARCHAR(20))
begin
    DECLARE id_room INT;

    SELECT id_type INTO id_room
    FROM room_type
    WHERE name_type=p_room;

    INSERT INTO apply_promotion(id_promotion, id_type) VALUES (p_id, id_room);
end;