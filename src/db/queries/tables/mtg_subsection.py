UPSERT = """
         INSERT INTO mtg_rule_subsection (id, section_id, title)
         VALUES ($1, $2, $3)
         ON CONFLICT (id) DO UPDATE SET title = excluded.title, section_id = excluded.section_id;
         """
