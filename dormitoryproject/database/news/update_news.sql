CREATE PROCEDURE update_news(IN _id_news INT, IN _id_staff INT, IN _title VARCHAR(20), IN _description VARCHAR(400))
BEGIN
    UPDATE news
    SET id_staff = IF(_id_staff is null, id_staff, _id_staff),
        title = IF(_title is null, title, _title),
        description = IF(_description is null, description, _description)
    WHERE id_news = _id_news;
end;