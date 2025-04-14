ALTER TABLE ebdb.check_ins
CHANGE insuranceImage insuranceImageFront TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE ebdb.check_ins
ADD COLUMN insuranceImageBack TINYINT(1) NOT NULL DEFAULT 0;