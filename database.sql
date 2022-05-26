drop database if exists `school`;
create database if not exists `school`;
use `school`;

drop table if exists `student`;
create table `student`
(
    `id` int NOT NULL AUTO_INCREMENT,
    `password` varchar(255),
    `name` varchar(255),
    `age` int,
    `gender` varchar(15),
    `grade` varchar(15),
    `school_year` int,
    primary key (`id`)
) character set utf8mb4;

insert into `student` (`password`, `name`, `age`, `gender`, `grade`, `school_year`) values 
("12345678", "Lê Văn A", 20, "nam", "DHCNTT01", 1),
("12345678", "Lê Thị B", 20, "nữ", "DHCNTT02", 1),
("12345678", "Nguyễn Văn C", 20, "nam", "DHCNTT01", 1),
("12345678", "Vũ Hồng D", 19, "nữ", "DHCNTT01", 1),
("12345678", "Lê Bình E", 19, "nam", "DHCNTT03", 2),
("12345678", "Đào Thị F", 18, "nữ", "DHCNTT05", 2);

drop table if exists `log`;
create table `log`
(
    `id` int NOT NULL AUTO_INCREMENT,
    `actor` int,
    `action` varchar(255),
    `detail` varchar(255),
    `subject` int,
    `table` varchar(255),
    `time` datetime,
    primary key (`id`)
);

insert into `log` (`actor`, `action`, `detail`, `subject`, `table`, `time`) values 
(1, "post", "created log table in database", 0, "log", now());

select * from `student`;
select * from `log`;