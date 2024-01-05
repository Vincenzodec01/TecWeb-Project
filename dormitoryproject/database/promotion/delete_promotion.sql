CREATE PROCEDURE delete_promotion(IN id_p INT)
BEGIN
    DELETE FROM apply_promotion WHERE id_promotion=id_p;
    DELETE FROM promotion WHERE id_promotion=id_p;
end;