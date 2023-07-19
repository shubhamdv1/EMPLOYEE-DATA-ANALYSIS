--------------------fact_fact_leave_status-----------



DELIMITER $$
CREATE PROCEDURE InsertLeaveStatus()
BEGIN
   INSERT INTO essl.fact_leave_status (employee_id, employee_name, attendance_date, isonleave, half_day)
    SELECT al.EmployeeId,
        emp.EmployeeName,
        DATE(al.AttendanceDate) AS attendance_date,
        (punchrecords IS NULL OR TRIM(punchrecords) = '') AS isonleave,
        NOT (punchrecords IS NULL OR TRIM(punchrecords) = '') AS half_day
    FROM sys.attendancelogs AS al
    INNER JOIN sys.employees AS emp ON emp.EmployeeId = al.EmployeeId
    WHERE (al.Status = 'Absent')
        AND (al.Status != 'Weekly Off' AND DAYOFWEEK(al.AttendanceDate) NOT IN (1, 7))
        AND al.Holiday != 1
    ORDER BY DATE(attendance_date);

END$$
DELIMITER ;
