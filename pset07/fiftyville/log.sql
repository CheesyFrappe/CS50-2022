-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT transcript FROM interviews WHERE day = 28 AND month = 7 -- The crime transcript
SELECT hour,destination_airport_id FROM flights WHERE day = 29 AND month = 7 -- The flight id of the escape
SELECT full_name, city FROM airports WHERE id = 4 -- The Airport and the city where they arrived after the crime

--SUSPECTS Bruce,Taylor
-- Taylor [License Plate] = 1106N58

-- Bruce [License Plate = 94KL13X] | [Number = (367) 555- 5533] -
-- (Accomplice's Number = (375) 555-8161 ) Name = Robin
