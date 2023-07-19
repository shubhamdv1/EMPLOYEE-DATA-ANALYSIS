CREATE EVENT stp_UpdateAttendanceAndEmployees_event
ON SCHEDULE
    EVERY 1 DAY
    STARTS '2023-04-28 06:00:00'
DO
    CALL stp_UpdateAttendanceAndEmployees();
