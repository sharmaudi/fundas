select * from public.annual_standalone where annual_standalone."symbol" = 'ITC';

create index ix_symbol on annual_standalone(symbol);