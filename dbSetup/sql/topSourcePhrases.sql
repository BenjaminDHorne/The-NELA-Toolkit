drop table if exists topSourcePhrases;
create table topSourcePhrases(
source varchar(255),
month smallint,
year smallint,
phrase1 varchar(255),
phrase2 varchar(255),
phrase3 varchar(255),
phrase4 varchar(255),
phrase5 varchar(255),
phrase6 varchar(255),
phrase7 varchar(255),
phrase8 varchar(255),
phrase9 varchar(255),
phrase10 varchar(255),
PRIMARY KEY(source, month)
);