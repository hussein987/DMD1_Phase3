-- Queries
PREPARE Query1 AS
    SELECT DISTINCT doctor_id, first_name, last_name, date
    FROM doctors d
             INNER JOIN appointment p ON d.ssn = p.doctor_id
    WHERE patient_id = $1
      AND date = (SELECT a.date from appointment a where a.date < now() and a.patient_id = $1 ORDER BY date DESC LIMIT 1)
      AND (first_name similar to '[ML][a-z]+'
        OR last_name similar to '[ML][a-z]+'
               AND NOT (first_name similar to '[ML][a-z]+' AND last_name similar to '[ML][a-z]+'));

------------------------------------------------------------

CREATE FUNCTION weekOf(d timestamp)
    RETURNS integer AS
$func$
BEGIN
    RETURN EXTRACT(WEEK FROM d);
END
$func$ LANGUAGE plpgsql;

CREATE FUNCTION yearOf(d timestamp)
    RETURNS integer AS
$func$
BEGIN
    RETURN EXTRACT(YEAR FROM d);
END
$func$ LANGUAGE plpgsql;

CREATE OR REPLACE VIEW doctor_stats_helper AS
SELECT a1.doctor_id,
       weekOf(a1.date) AS week,
       a1.slot
FROM appointment a1
WHERE a1.date >= current_date - INTERVAL '1 year'
  and a1.date <= current_date
GROUP BY a1.doctor_id, weekOf(a1.date), a1.slot;

CREATE OR REPLACE VIEW doctors_weeks_stats AS
SELECT *,
       (SELECT count(*)
        FROM appointment a
        WHERE h.doctor_id = a.doctor_id
          and weekOf(a.date) = h.week
          and a.slot = h.slot
          and a.date >= current_date - INTERVAL '1 year'
          and a.date <= current_date) as appointments
FROM doctor_stats_helper h;

PREPARE Query2 AS SELECT doctor_id, slot, sum(appointments) / 52 as avg, sum(appointments)
                  FROM doctors_weeks_stats
                  GROUP BY doctor_id, slot;

------------------------------------------------------------

CREATE OR REPLACE VIEW patient_stats_helper AS
SELECT patient_id,
       weekOf(date) AS week
FROM Appointment
WHERE date >= current_date - INTERVAL '1 month'
  and date <= current_date
GROUP BY patient_id, week;

CREATE OR REPLACE VIEW patient_weeks_stats AS
SELECT *,
       (SELECT count(*)
        FROM appointment a
        WHERE h.patient_id = a.patient_id
          AND date >= current_date - INTERVAL '1 month'
          and date <= current_date
          AND weekOf(a.date) = h.week) AS appointments
FROM patient_stats_helper h;

CREATE OR REPLACE FUNCTION weeks_count_last_month()
    RETURNS integer AS
$func$
BEGIN
    return (select count(*)
            from (select distinct extract(week from generate_series(current_date - '1 month'::interval, current_date,
                                                                    '1 day'::interval))) as weeks);
END
$func$ LANGUAGE plpgsql;

PREPARE Query3 AS SELECT DISTINCT patient_id, name as full_name
                  FROM patient_weeks_stats stats
                           INNER JOIN patient p on p.medical_insurance_id = stats.patient_id
                  WHERE (SELECT count(*)
                         from patient_weeks_stats s
                         where s.patient_id = stats.patient_id
                           and s.appointments >= 2) = weeks_count_last_month();

--------------------------------------------------------

CREATE OR REPLACE VIEW last_month_appointments AS
SELECT  distinct A.patient_id,
       (EXTRACT(year FROM age(current_date,P.birthday)))::integer as age,
       (SELECT count(A1.patient_id)
        FROM appointment A1
        WHERE A1.patient_id = A.patient_id
           AND date >= current_date - INTERVAL '1 month' and date <= current_date ) as appointments
FROM appointment A, patient P
WHERE P.medical_insurance_id = A.patient_id AND date >= current_date - INTERVAL '1 month' and date <= current_date;

CREATE OR REPLACE VIEW income AS
    SELECT
    (SELECT count(*)
    FROM last_month_appointments
    WHERE age < 50 AND appointments < 3)*200 as value1,
    (SELECT count(*)
    FROM last_month_appointments
    WHERE age < 50  and appointments >= 3)*250 as value2,
    (SELECT  count(*)
    FROM last_month_appointments L
    WHERE age >= 50  and appointments < 3)*400 as value3,
    (SELECT count(*)
    FROM last_month_appointments L
    WHERE age >= 50 and appointments >= 3)*500 as value4;

PREPARE Query4 AS
    SELECT sum(value1 + value2 + value3 + value4)
    FROM income;


---------------------------------------------------------------

CREATE OR REPLACE VIEW doctor_year_report_helper AS
SELECT doctor_id,
       yearOf(date) AS year
FROM Appointment
WHERE date >= current_date - INTERVAL '10 year'
  and date <= current_date;

PREPARE Query5 AS with stats AS (SELECT *,
       (SELECT count(*)
        FROM appointment a
        WHERE h.doctor_id = a.doctor_id
          AND date >= current_date - INTERVAL '10 year'
          and date <= current_date
          AND yearOf(a.date) = h.year) AS year_appointments,

       (SELECT count(a.doctor_id)
       FROM appointment a
       WHERE a.doctor_id = h.doctor_id
         AND date >= current_date - INTERVAL '10 year') as decade_appointments
FROM doctor_year_report_helper h)

SELECT distinct doctor_id, decade_appointments
from stats p
where not exists(select doctor_id from stats p2 where p2.doctor_id = p.doctor_id and p2.year_appointments < 5) and p.decade_appointments >= 100;