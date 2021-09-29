TYPE=TRIGGERS
triggers='CREATE DEFINER=`admin`@`%` TRIGGER update_bills_paid_tbl\n	AFTER INSERT ON bills_bill\n	FOR EACH ROW\n	BEGIN\n		INSERT INTO bills_billpaid\n			(paidDate, notes, paidBool, totalPaid, billID_id)\n			VALUES(NULL, "N/A", 0, NEW.charge + NEW.anc_fees + NEW.taxes + NEW.credit, NEW.billID);\n			\n	END'
sql_modes=1411383296
definers='admin@%'
client_cs_names='utf8mb4'
connection_cl_names='utf8mb4_general_ci'
db_cl_names='utf8mb4_general_ci'
created=163294203085
