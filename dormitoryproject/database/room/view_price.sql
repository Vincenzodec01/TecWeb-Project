CREATE PROCEDURE view_price(IN id_room INT, OUT price FLOAT)
BEGIN
    SELECT IF(p1.id_promotion, r.price - r.price*p2.percent_discount/100, r.price) INTO price
    FROM room_type r
    LEFT JOIN apply_promotion p1 on r.id_type = p1.id_type
    LEFT JOIN promotion p2 on p1.id_promotion = p2.id_promotion
    WHERE r.id_type = id_room or (p2.p_start_date <= now() and p2.p_end_date >= now() and r.id_type=id_room and p1.id_promotion is not null);
end;