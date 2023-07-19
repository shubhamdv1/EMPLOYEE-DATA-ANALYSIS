DELIMITER $$
CREATE PROCEDURE stp_UpdateAttendanceAndEmployees()
BEGIN
    -- Insert new attendance logs into stg_attendancelogs table
    INSERT INTO essl.stg_attendancelogs (
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
        essl.attendancelogs
    WHERE 
	   (TRIM(punchrecords) != '')  AND
        attendancelogid NOT IN (
            SELECT 
                attendance_log_id 
            FROM 
                essl.stg_attendancelogs
        );
        
    -- Insert new employees into stg_employees table
    INSERT INTO essl.stg_employees (employee_id, employee_name, employee_code, status, company_id)
    SELECT EmployeeId, EmployeeName, EmployeeCode, Status,CompanyId
    FROM essl.Employees
    WHERE EmployeeId NOT IN (
        SELECT employee_id
        FROM essl.stg_employees
    );
END$$
DELIMITER ;
