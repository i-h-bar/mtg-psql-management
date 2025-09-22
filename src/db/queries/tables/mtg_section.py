UPSERT = """
         INSERT INTO mtg_rule_section (id, name)
         VALUES ($1, $2)
         ON CONFLICT (id) DO UPDATE SET name = $2;
         """
