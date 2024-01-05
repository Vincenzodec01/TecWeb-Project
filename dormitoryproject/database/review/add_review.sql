CREATE PROCEDURE add_review(IN _title VARCHAR(20), IN _description VARCHAR(400), IN _vote INT, IN _id_reserv INT)
BEGIN
    INSERT INTO review(review_id, vote, title, description, review_date, id_reservation)
    VALUES (default, _vote, _title, _description, NOW(), _id_reserv);
end;