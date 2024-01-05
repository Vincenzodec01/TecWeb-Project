CREATE PROCEDURE modify_promotion(IN id_p INT, IN name_p VARCHAR(20), IN start_date TIMESTAMP, IN end_date TIMESTAMP, IN percent INT)
BEGIN
    UPDATE promotion
    SET promotion_name = IF(name_p is not null, name_p, promotion_name),
        p_start_date = IF(start_date is not null, start_date, p_start_date),
        p_end_date = IF(end_date is not null, end_date, p_end_date),
        percent_discount = IF(percent is not null, percent, percent_discount)
    WHERE id_promotion=id_p;
end;