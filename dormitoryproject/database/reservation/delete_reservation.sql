CREATE PROCEDURE delete_reservation(IN _id_reservation INT)
BEGIN
    DELETE FROM reservation WHERE id_reservation = _id_reservation;
end;