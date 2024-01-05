CREATE PROCEDURE delete_news(IN _id_news INT)
BEGIN
    DELETE FROM news WHERE id_news = _id_news;
end;