CREATE PROCEDURE add_type_room(IN _name_type VARCHAR(20),IN _description VARCHAR(400), IN _price FLOAT, IN _adults INT)
BEGIN
    INSERT INTO room_type(id_type, name_type, adults, price, description) VALUES (0, _name_type, _price, _description, _adults);
end;

commit;
