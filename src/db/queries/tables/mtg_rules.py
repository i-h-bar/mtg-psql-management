INSERT = """
         INSERT INTO mtg_rules (rule_number, parent_rule, section_number, section_title,
                                subsection_number, subsection_title, content)
         VALUES ($1, $2, $3, $4, $5, $6, $7)
         ON CONFLICT(rule_number) DO UPDATE SET rule_number       = EXCLUDED.rule_number,
                                                parent_rule       = EXCLUDED.parent_rule,
                                                section_number    = EXCLUDED.section_number,
                                                section_title     = EXCLUDED.section_title,
                                                subsection_number = EXCLUDED.subsection_number,
                                                subsection_title  = EXCLUDED.subsection_title,
                                                content           = EXCLUDED.content;
         """
