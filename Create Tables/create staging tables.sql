---------------create staging tables------------------

CREATE TABLE stg_attendancelogs (
employee_id numeric,
attendance_log_id numeric,
attendance_date date,
in_device_id varchar(50),
out_device_id varchar(50),
in_time datetime,
out_time datetime,
duration numeric,
loss_of_hours numeric,
punch_records varchar(10000)
);

--------------------------------------------

CREATE TABLE essl.stg_employees (
employee_id bigint,
employee_code text,
employee_name text,
company_id int,
status text
);