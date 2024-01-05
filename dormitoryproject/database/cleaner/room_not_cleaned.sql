CREATE VIEW view_room_not_cleaned AS
SELECT r.room_number
FROM
(SELECT r.room_number, max(check_out_date) as max_check_out
FROM reservation r
GROUP BY r.room_number) r
LEFT JOIN
(SELECT c.room_number, max(cleaning_date) as max_clean_date
FROM cleaning c
GROUP BY c.room_number
) c on r.room_number = c.room_number
WHERE c.max_clean_date is null or r.max_check_out > c.max_clean_date and max_check_out <= now();


