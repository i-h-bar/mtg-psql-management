INSERT = """
         INSERT INTO mtg_glossary (term, definition, rule_references)
         VALUES ($1, $2, $3)
         ON CONFLICT(term) DO UPDATE SET term            = EXCLUDED.term,
                                         definition      = EXCLUDED.definition,
                                         rule_references = EXCLUDED.rule_references;
         """
