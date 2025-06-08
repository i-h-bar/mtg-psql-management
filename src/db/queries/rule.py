INSERT = """
INSERT INTO rule (id, colour_identity, mana_cost, cmc, power, toughness, loyalty, defence, type_line,
oracle_text, colours, keywords, produced_mana, rulings_url)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14) ON CONFLICT DO NOTHING
"""
