drop table if exists sourcePublishCounts;
create table sourcePublishCounts(
source varchar(255),
month smallint,
count int,
PRIMARY KEY(source, month)
);