CREATE TABLE script_details (
    script_id INT NOT NULL PRIMARY KEY,
    script_name VARCHAR(255) NOT NULL,
    frequency VARCHAR(50),
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE script_audit_log (
    log_id BIGINT NOT NULL AUTO_INCREMENT,
    script_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME DEFAULT NULL,
    status VARCHAR(20),
    load_date DATE NOT NULL,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id),
    INDEX idx_date_script (load_date, script_id),
    CONSTRAINT fk_script FOREIGN KEY (script_id) REFERENCES script_details(script_id)
);

ALTER TABLE audit_log ADD INDEX idx_report_lookup (load_date, script_id);


CREATE OR REPLACE VIEW vw_jedox_audit_summary AS
SELECT 
    s.script_name,
    al.start_time,
    al.end_time,
    CASE 
        WHEN al.log_id IS NULL THEN 'MISSING (Did not trigger)'
        WHEN al.end_time IS NULL AND al.status = 'Running' THEN 'FAILED (Crashed/Timed out)'
        ELSE al.status 
    END AS final_status
FROM script_details s
LEFT JOIN (
    -- Get only the last record for each script for today
    SELECT * FROM audit_log 
    WHERE log_id IN (
        SELECT MAX(log_id) FROM audit_log WHERE load_date = CURDATE() GROUP BY script_id
    )
) al ON s.script_id = al.script_id
WHERE s.is_active = 1;


DELIMITER //

CREATE PROCEDURE sp_manage_audit_log(
    IN p_script_id INT,
    IN p_action VARCHAR(10), -- (START,END)
    IN p_status VARCHAR(20)  -- (Success, Failed)
)
BEGIN
    DECLARE v_start_time DATETIME;
    IF p_action = 'END' THEN
        SELECT start_time INTO v_start_time 
        FROM audit_log 
        WHERE script_id = p_script_id 
          AND load_date = CURDATE()
          AND end_time IS NULL
        ORDER BY log_id DESC LIMIT 1;
        
        INSERT INTO audit_log (script_id, start_time, end_time, status, load_date)
        VALUES (p_script_id, v_start_time, NOW(), p_status, CURDATE());
        
    ELSE
        INSERT INTO audit_log (script_id, start_time, end_time, status, load_date)
        VALUES (p_script_id, NOW(), NULL, p_status, CURDATE());
    END IF;
END //

DELIMITER ;