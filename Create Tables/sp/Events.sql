
---------------------------event-1-----------------------------------

DELIMITER $$
CREATE EVENT raw_table_to_stg_table
ON SCHEDULE
  EVERY 2 HOUR
  STARTS CURRENT_TIMESTAMP
DO
  CALL stp_UpdateAttendanceAndEmployees();
$$
DELIMITER ;




----------------------------------event-2-------------------------------------


DELIMITER $$
CREATE EVENT fact_attendancelogs_event
ON SCHEDULE
  EVERY 2 HOUR
  STARTS CURRENT_TIMESTAMP
DO
  CALL InsertLeaveStatus();
$$
DELIMITER ;


----------------------------------event-3-----------------------------------

DELIMITER $$
CREATE EVENT fact_LeaveStatus_event
ON SCHEDULE
  EVERY 2 HOUR
  STARTS CURRENT_TIMESTAMP
DO
  CALL InsertLeaveStatus();
$$
DELIMITER ;