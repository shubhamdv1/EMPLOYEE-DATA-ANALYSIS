--------------------fact_attendance_logs table stored procedure-----------

DELIMITER $$

CREATE PROCEDURE sp_insert_attendance_logs()
BEGIN

    INSERT INTO fact_attendance_logs (employee_id,employee_name, employee_code, attendance_date, duration, break_time, net_hours)
    SELECT 
	   emp.employee_id,
        emp.employee_name,
        emp.employee_code, 
        sa.attendance_date,
        TIME_FORMAT(SEC_TO_TIME(sa.duration*60), '%H:%i') AS duration,
        TIME_FORMAT(SEC_TO_TIME(dabt.break_in_minutes*60), '%H:%i') AS break_time,
        TIME_FORMAT(SEC_TO_TIME((sa.duration - dabt.break_in_minutes)*60), '%H:%i') AS net_hours
    FROM 
        dim_attendance_break_time dabt
        INNER JOIN stg_attendancelogs sa 
            ON dabt.employee_id = sa.employee_id 
            AND dabt.attendance_date = sa.attendance_date
    	INNER JOIN stg_employees as emp
            ON emp.employee_id = sa.employee_id 
    WHERE 
		 emp.status = 'Working'
		AND emp.company_id NOT IN  ('1')
    ORDER BY 
        sa.employee_id,
        sa.attendance_date;

END $$

DELIMITER ;
