CREATE PROCEDURE search_reservation(IN id INT)
BEGIN
    SELECT *
    FROM reservation
    WHERE id_reservation = id;
end;