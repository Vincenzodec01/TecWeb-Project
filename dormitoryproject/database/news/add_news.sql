CREATE PROCEDURE add_news(IN _id_staff INT, IN _title VARCHAR(20), IN _description VARCHAR(400))
BEGIN
    INSERT INTO news(id_news, title, publication_date, description, id_staff)
    VALUES (default, _title, NOW(), _description, _id_staff);
end;