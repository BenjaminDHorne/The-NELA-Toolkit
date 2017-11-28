create index day_idx on articleFeatures(datePublished, source);
cluster articleFeatures using day_idx;

CREATE OR REPLACE FUNCTION _final_median(FLOAT[])
   RETURNS FLOAT AS
$$
   SELECT AVG(val)
   FROM (
     SELECT val
     FROM unnest($1) val
     ORDER BY 1
     LIMIT  2 - MOD(array_upper($1, 1), 2)
     OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
   ) sub;
$$
LANGUAGE 'sql' IMMUTABLE;
 
CREATE AGGREGATE median(FLOAT) (
  SFUNC=array_append,
  STYPE=FLOAT[],
  FINALFUNC=_final_median,
  INITCOND='{}'
);

analyze;
