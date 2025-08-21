DROP_TABLES = """
DO $$
DECLARE
    tbl RECORD;
BEGIN
    FOR tbl IN
        SELECT tablename, schemaname
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        RAISE NOTICE 'Dropping table: %.%', quote_ident(tbl.schemaname), quote_ident(tbl.tablename);
        EXECUTE format('DROP TABLE %I.%I CASCADE;', tbl.schemaname, tbl.tablename);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
"""
