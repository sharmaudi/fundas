DROP MATERIALIZED VIEW latest_c_a;
DROP MATERIALIZED VIEW latest_s_a;
DROP MATERIALIZED VIEW latest_c_q;
DROP MATERIALIZED VIEW latest_s_q;


create MATERIALIZED VIEW latest_c_a as
  SELECT  DISTINCT  on ("symbol") *
  from annual_consolidated
  ORDER BY "symbol", "date" DESC NULLS LAST;

create MATERIALIZED VIEW latest_s_a as
  SELECT  DISTINCT  on ("symbol") *
  from annual_standalone
  ORDER BY "symbol", "date" DESC NULLS LAST;

create MATERIALIZED VIEW latest_c_q as
  SELECT  DISTINCT  on ("symbol") *
  from quarterly_consolidated
  ORDER BY "symbol", "date" DESC NULLS LAST;

create MATERIALIZED VIEW latest_s_q as
  SELECT  DISTINCT  on ("symbol") *
  from quarterly_standalone
  ORDER BY "symbol", "date" DESC NULLS LAST

CREATE UNIQUE INDEX idx_symbol_c_a on latest_c_a(symbol);
CREATE UNIQUE INDEX idx_symbol_s_a on latest_s_a(symbol);
CREATE UNIQUE INDEX idx_symbol_c_q on latest_c_q(symbol);
CREATE UNIQUE INDEX idx_symbol_s_q on latest_c_q(symbol);
