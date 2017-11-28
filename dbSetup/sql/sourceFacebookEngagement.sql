drop table if exists sourceFacebookEngagement;
create table sourceFacebookEngagement(
source varchar(255),
month smallint,
FB_Comment_Counts integer,
FB_Share_Counts integer,
FB_Reaction_Counts integer,
PRIMARY KEY(source, month)
);