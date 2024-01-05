CREATE PROCEDURE check_user(IN username CHAR(16), IN password VARCHAR(64), OUT found INT)
BEGIN
    SELECT count(*) INTO found
    FROM user u
    WHERE fiscal_code=username and u.password=sha2(password, 256);
end;
