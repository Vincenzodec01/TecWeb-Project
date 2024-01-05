CREATE PROCEDURE check_staff(IN username CHAR(16), IN password VARCHAR(64), OUT found INT)
BEGIN
    SELECT count(*) INTO found
    FROM staff s
    WHERE s_fiscal_code=username and s.s_password=sha2(password, 256);
end;
commit;