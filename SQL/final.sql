SELECT 
    emp.employee_name,
    emp.employee_code, 
    sa.attendance_date,
    TIME_FORMAT(SEC_TO_TIME(sa.duration*60), '%H:%i') AS duration,
    TIME_FORMAT(SEC_TO_TIME(dabt.break_in_minutes*60), '%H:%i') AS break_time,
    TIME_FORMAT(SEC_TO_TIME((sa.duration - dabt.break_in_minutes)*60), '%H:%i') AS net_duration
FROM 
    dim_attendance_break_time dabt
    INNER JOIN stg_attendancelogs sa 
        ON dabt.employee_id = sa.employee_id 
        AND dabt.attendance_date = sa.attendance_date
	INNER JOIN stg_employees as emp
        ON emp.employee_id = sa.employee_id 
	
WHERE 
    sa.in_device_id = 'IN'
    AND sa.out_device_id = 'OUT'
ORDER BY 
    sa.employee_id,
    sa.attendance_date;