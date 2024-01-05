CREATE PROCEDURE add_reservation(IN _check_in_date timestamp, IN _check_out_date timestamp, IN _id_user INT, IN _name_type VARCHAR(20), IN _price FLOAT)
BEGIN
    DECLARE id_name INT;
    DECLARE _id_reserv INT;
    DECLARE num_room CHAR(3);
    SELECT id_type INTO id_name FROM room_type WHERE name_type = _name_type;

    SET _check_in_date = DATE_ADD(_check_in_date, INTERVAL 10 HOUR);
    SET _check_out_date = DATE_ADD(_check_out_date, INTERVAL 10 HOUR);

    SELECT room_number INTO num_room
    FROM room
    WHERE id_type = id_name and room_number NOT IN
    (SELECT r1.room_number
    FROM room r1
    JOIN reservation r2 on r1.room_number = r2.room_number
    WHERE r2.check_out_date >= _check_out_date and r2.check_in_date <= _check_in_date)
    LIMIT 1;

    INSERT INTO reservation(id_reservation, check_in_date, check_out_date, reservation_date, start_date, end_date, id_type, room_number)
    VALUES (0, _check_in_date, _check_out_date, NOW(), null, null, id_name, num_room);
    SELECT LAST_INSERT_ID() INTO _id_reserv;
    INSERT INTO reservation_user(id_user, id_reservation) VALUES (_id_user, _id_reserv);

    INSERT INTO payment (id_payment, receipt_number, total, payment_date, id_reservation) VALUES (0, null, _price, NOW(), _id_reserv);

end;
