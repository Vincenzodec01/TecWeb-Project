CREATE PROCEDURE delete_staff(IN id_staff INT)
BEGIN
    DELETE FROM staff s WHERE s.id_staff = id_staff;
end;