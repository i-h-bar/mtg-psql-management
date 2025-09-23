UPSERT = """
         INSERT INTO mtg_rule_section (id, title)
         VALUES ($1, $2)
         ON CONFLICT (id) DO UPDATE SET title = excluded.title;
         """
