SELECT t2.id_type, t2.name_type, t1.available
FROM
(SELECT t1.id_type, (total_room - busy_room) as available
FROM
(SELECT id_type, count(*) AS busy_room
FROM reservation
WHERE (check_in_date <= CURDATE() and check_out_date >= CURDATE() and end_date is null) or (check_in_date <= CURDATE() and end_date >= CURDATE())
GROUP BY id_type) t1
JOIN
(SELECT id_type, count(*) AS total_room
FROM room
GROUP BY id_type) t2 ON t1.id_type = t2.id_type) t1
JOIN
room_type t2 on t1.id_type=t2.id_type
WHERE t2.adults = adults