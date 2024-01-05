CREATE PROCEDURE delete_user(IN id_user INT)
BEGIN
    DELETE FROM user u WHERE u.id_user = id_user;
end;