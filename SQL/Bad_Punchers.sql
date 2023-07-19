----------Bad Punchers employee count-----

SELECT 
  employee_id, 
  COUNT(*) 
FROM 
  dim_attendance_records 
WHERE 
  (punch_in = '00:00:00' OR punch_out = '00:00:00') 
GROUP BY 
  employee_id 
ORDER BY 
  employee_id ASC;