CREATE PROCEDURE update_user(IN _id_user INT, IN _email VARCHAR(60))
BEGIN
    UPDATE user
    SET email = IF(_email is null, email, _email)
    WHERE id_user=_id_user;
end;