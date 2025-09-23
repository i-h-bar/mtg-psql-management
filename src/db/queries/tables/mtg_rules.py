UPSERT = """
         INSERT INTO mtg_rule (rule_number, parent_rule, subsection_id, content)
         VALUES ($1, $2, $3, $4)
         ON CONFLICT(rule_number) DO UPDATE SET rule_number   = EXCLUDED.rule_number,
                                                parent_rule   = EXCLUDED.parent_rule,
                                                subsection_id = EXCLUDED.subsection_id,
                                                content       = EXCLUDED.content;
         """
