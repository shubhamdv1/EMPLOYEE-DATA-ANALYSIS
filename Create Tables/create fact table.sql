CREATE TABLE fact_attendance_logs (
 employee_id INT, 
employee_code varchar (100),
employee_name varchar (500),
attendance_date DATE,
duration TIME,
break_time TIME,
net_hours TIME
);


CREATE TABLE fact_leave_status (
  employee_id INT,
  employee_name varchar(500),
  attendance_date DATE,
  isonleave INT,
  half_day INT
);