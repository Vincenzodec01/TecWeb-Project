CREATE VIEW view_promotion as
SELECT p.id_promotion, p.promotion_name, p.p_start_date, p.p_end_date, p.percent_discount, r.name_type
FROM
(promotion p
JOIN apply_promotion a on p.id_promotion = a.id_promotion
JOIN room_type r on a.id_type = r.id_type);

