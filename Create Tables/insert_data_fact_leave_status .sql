-----------------fact_leave_status---------------------


INSERT INTO fact_leave_status (employee_id, employee_name, attendance_date, isonleave, half_day)
SELECT al.EmployeeId,
emp.EmployeeName,
 DATE(al.AttendanceDate) AS attendance_date,
  (punchrecords IS NULL OR TRIM(punchrecords) = '') as isonleave,
 NOT (punchrecords IS NULL OR TRIM(punchrecords) = '') as half_day
FROM attendancelogs as al
INNER JOIN employees AS emp
ON emp.EmployeeId = al.EmployeeId
WHERE (al.Status = 'Absent')
   AND (al.Status != 'Weekly Off' and  DAYOFWEEK(al.AttendanceDate) NOT IN (1, 7))
   AND al.Holiday != 1
ORDER BY DATE(attendance_date)