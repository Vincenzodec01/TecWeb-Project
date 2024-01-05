CREATE PROCEDURE create_staff(IN fiscal_code CHAR(16),IN _password VARCHAR(64), IN name VARCHAR(20), IN surname VARCHAR(20), IN email VARCHAR(50), IN gender CHAR(1), IN _role VARCHAR(15), IN phone_number VARCHAR(10), IN secret CHAR(32))
BEGIN
    INSERT INTO staff(id_staff, s_fiscal_code, s_password, s_name, s_surname, s_email, s_gender, role, phone, secret_key, access)
    VALUES (default, fiscal_code, sha2(_password, 256), name, surname, email, gender, _role, phone_number, secret, 0);
end;
