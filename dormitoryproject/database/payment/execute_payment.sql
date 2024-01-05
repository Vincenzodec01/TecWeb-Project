CREATE PROCEDURE execute_payment(IN _total FLOAT, IN _id_reservation INT)
begin
    INSERT INTO payment(receipt_number, total, payment_date, id_reservation)
    VALUES (gen_key(6), _total, NOW(), _id_reservation);
end;