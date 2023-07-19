
CREATE TABLE IF NOT EXISTS dim_attendance_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(255) NOT NULL,
    attendance_log_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    punch_in TIME NOT NULL,
    punch_out TIME NOT NULL
)

CREATE TABLE IF NOT EXISTS dim_attendance_time (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(255) NOT NULL,
    attendance_log_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    punch_in TIME NOT NULL,
    punch_out TIME NOT NULL
)

CREATE TABLE IF NOT EXISTS dim_attendance_break_time (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(255) NOT NULL,
    attendance_date DATE NOT NULL,
    break_in_minutes INT NOT NULL
    );
