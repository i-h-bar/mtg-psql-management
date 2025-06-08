INSERT = """INSERT INTO card
(id, oracle_id, name, normalised_name, scryfall_url, flavour_text, release_date, reserved, rarity, artist_id,
image_id, illustration_id, legality_id, rule_id, set_id, backside_id)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)ON CONFLICT DO NOTHING
"""
