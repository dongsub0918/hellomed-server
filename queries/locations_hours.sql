create table ebdb.locations (
	code varchar(32) primary key not null,
    title varchar(64) not null,
    address varchar(64) not null,
    holiday_start datetime,
    holiday_end datetime,
    holiday_message varchar(128),
    mon varchar(64),
    tue varchar(64),
    wed varchar(64),
    thu varchar(64),
    fri varchar(64),
    sat varchar(64),
    sun varchar(64),
    lunch_break varchar(64),
    open tinyint
);

INSERT INTO ebdb.locations (code, title, address, holiday_start, holiday_end, holiday_message, 
    mon, tue, wed, thu, fri, sat, sun, lunch_break, open) 
VALUES 
    ('HELLOMED_Central', 'HELLOMED Central', '625 E Liberty St, Ann Arbor', NULL, NULL, NULL, 
     '9:10 am - 6:00 pm', '9:10 am - 6:00 pm', '9:00 am - 6:00 pm', '9:10 am - 6:00 pm', '9:10 am - 5:00 pm', 
     '', '', '1:00 pm - 1:30 pm', 1),
    
    ('HELLOMED_North', 'HELLOMED North', '2731 Plymouth Rd, Ann Arbor', NULL, NULL, NULL, 
     '9:00 am - 6:00 pm', '', '9:00 am - 6:00 pm', '9:00 am - 6:00 pm', '9:00 am - 6:00 pm', 
     '10:00 am - 11:30 am (Immigration Medical Exam only)', '', '1:30 pm - 2:00 pm', 1),
    
    ('HELLOMED_South', 'HELLOMED South (Inside Meijer)', '', NULL, NULL, '', 
     '', '', '', '', '', '', '', '', 0);

alter table ebdb.check_ins
add column viewed tinyint not null default 0;
