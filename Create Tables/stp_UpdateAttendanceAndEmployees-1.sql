DELIMITER $$
CREATE PROCEDURE stp_UpdateAttendanceAndEmployees()
BEGIN
    -- Insert new attendance logs into stg_attendancelogs table
    INSERT INTO stg_attendancelogs (
        employee_id, 
        attendance_log_id, 
        attendance_date, 
        in_device_id, 
        out_device_id, 
        in_time, 
        out_time, 
        duration,
        punch_records
    )
    SELECT 
        EmployeeId, 
        attendancelogid, 
        AttendanceDate, 
        InDeviceId, 
        OutDeviceId, 
        InTime, 
        OutTime, 
        Duration,
        PunchRecords
    FROM 
        sys.attendancelogs
    WHERE
      AND 	
        attendancelogid NOT IN (
            SELECT 
                attendance_log_id 
            FROM 
                stg_attendancelogs
        );
        
    -- Insert new employees into stg_employees table
    INSERT INTO sys.stg_employees (employee_id, employee_name, employee_code, status)
    SELECT EmployeeId, EmployeeName, EmployeeCode, Status
    FROM sys.Employees
    WHERE EmployeeId NOT IN (
        SELECT employee_id
        FROM sys.stg_employees
    );
END$$
DELIMITER ;
