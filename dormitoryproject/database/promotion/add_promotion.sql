CREATE PROCEDURE add_promotion(IN p_name VARCHAR(20), IN start TIMESTAMP, IN end TIMESTAMP, IN discount INT)
BEGIN

    INSERT INTO promotion(id_promotion, promotion_name, p_start_date, p_end_date, percent_discount)
    VALUES (0, p_name, start, end, discount);

end;