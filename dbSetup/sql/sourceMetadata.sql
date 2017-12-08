drop table if exists sourceMetadata;
create table sourceMetadata(
source varchar(255) PRIMARY KEY,
perCredible float,
perImpartial float,
satireFlag float,
dateComputed date);