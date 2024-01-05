DELIMITER //
create procedure add_clean_room(IN _id_staff int, IN _room_number char(3))
BEGIN
    INSERT INTO cleaning(cleaning_id, cleaning_date, room_number, id_staff) VALUES (0, NOW(), _room_number, _id_staff);
end;

create procedure add_promotion(IN p_name varchar(20), IN start timestamp, IN end timestamp,
                                                      IN discount int)
BEGIN

    INSERT INTO promotion(id_promotion, promotion_name, p_start_date, p_end_date, percent_discount)
    VALUES (0, p_name, start, end, discount);

end;


create procedure add_promotion_room(IN p_id int, IN p_room varchar(20))
begin
    DECLARE id_room INT;

    SELECT id_type INTO id_room
    FROM room_type
    WHERE name_type=p_room;

    INSERT INTO apply_promotion(id_promotion, id_type) VALUES (p_id, id_room);
end;

create procedure add_reservation(IN _check_in_date timestamp, IN _check_out_date timestamp,
                                                        IN _id_user int, IN _name_type varchar(20), IN _price float)
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

create procedure add_review(IN _title varchar(20), IN _description varchar(400), IN _vote int,
                                                   IN _id_reserv int)
BEGIN
    INSERT INTO review(review_id, vote, title, description, review_date, id_reservation)
    VALUES (default, _vote, _title, _description, NOW(), _id_reserv);
end;

create procedure add_room(IN _room_number char(3), IN _type_room varchar(20))
BEGIN
    DECLARE id_name INT;
    SELECT id_type INTO id_name FROM room_type WHERE name_type = _type_room;
    INSERT INTO room(room_number, id_type) VALUES (_room_number, id_name);
end;

create procedure add_type_room(IN _name_type varchar(20), IN _description varchar(400),
                                                      IN _price float, IN _adults int)
BEGIN
    INSERT INTO room_type(id_type, name_type, adults, price, description) VALUES (0, _name_type, _adults, _price, _description);
end;

create procedure check_staff(IN username char(16), IN password varchar(64), OUT found int)
BEGIN
    SELECT count(*) INTO found
    FROM staff s
    WHERE s_fiscal_code=username and s.s_password=sha2(password, 256);
end;

create procedure check_user(IN username char(16), IN password varchar(64), OUT found int)
BEGIN
    SELECT count(*) INTO found
    FROM user u
    WHERE fiscal_code=username and u.password=sha2(password, 256);
end;

create procedure create_staff(IN fiscal_code char(16), IN _password varchar(64),
                                                     IN name varchar(20), IN surname varchar(20), IN email varchar(50),
                                                     IN gender char, IN _role varchar(15), IN phone_number varchar(10),
                                                     IN secret char(32))
BEGIN
    INSERT INTO staff(id_staff, s_fiscal_code, s_password, s_name, s_surname, s_email, s_gender, role, phone, secret_key, access)
    VALUES (default, fiscal_code, sha2(_password, 256), name, surname, email, gender, _role, phone_number, secret, 0);
end;

create procedure create_user(IN matr char(10), IN _email varchar(60), IN _fiscal_code char(16),
                                                    IN _password varchar(64), IN _name varchar(20),
                                                    IN _surname varchar(20), IN _gender char, IN _role varchar(15))
BEGIN
    INSERT INTO user (id_user, matriculation_number, email, fiscal_code, password, name, surname, gender, role)
    VALUES (0, matr, _email, _fiscal_code, sha2(_password, 256), _name, _surname, _gender, _role);
end;

create procedure delete_promotion(IN id_p int)
BEGIN
    DELETE FROM apply_promotion WHERE id_promotion=id_p;
    DELETE FROM promotion WHERE id_promotion=id_p;
end;

create procedure delete_room(IN _room_number char(3))
BEGIN
    DELETE FROM room WHERE room_number = _room_number;
end;

create procedure delete_user(IN id_user int)
BEGIN
    DELETE FROM user u WHERE u.id_user = id_user;
end;

create procedure modify_promotion(IN id_p int, IN name_p varchar(20), IN start_date timestamp,
                                                         IN end_date timestamp, IN percent int)
BEGIN
    UPDATE promotion
    SET promotion_name = IF(name_p is not null, name_p, promotion_name),
        p_start_date = IF(start_date is not null, start_date, p_start_date),
        p_end_date = IF(end_date is not null, end_date, p_end_date),
        percent_discount = IF(percent is not null, percent, percent_discount)
    WHERE id_promotion=id_p;
end;

create procedure update_room(IN _room_number char(3), IN _room_type varchar(20))
BEGIN
    DECLARE _id_ INT;

    SELECT id_type INTO _id_ FROM room_type WHERE name_type=_room_type;

    UPDATE room
    SET room_number = _room_number,
        id_type = IF(_id_ is null, id_type, _id_)
    WHERE room_number = _room_number;
end;

create procedure view_price(IN id_room int, OUT price float)
BEGIN
    SELECT IF(p1.id_promotion, r.price - r.price*p2.percent_discount/100, r.price) INTO price
    FROM room_type r
    LEFT JOIN apply_promotion p1 on r.id_type = p1.id_type
    LEFT JOIN promotion p2 on p1.id_promotion = p2.id_promotion
    WHERE r.id_type = id_room or (p2.p_start_date <= now() and p2.p_end_date >= now() and r.id_type=id_room and p1.id_promotion is not null);
end;

DELIMITER ;