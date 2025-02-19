INSERT_ARTIST = "INSERT into artist (id, name, normalised_name) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING"

INSERT_ILLUSTRATION = "INSERT into illustration (id, illustration) VALUES ($1, $2) ON CONFLICT DO NOTHING"

INSERT_IMAGE = "INSERT into image (id, png) VALUES ($1, $2) ON CONFLICT DO NOTHING"

INSERT_LEGALITY = """
INSERT INTO legality
(id, alchemy, brawl, commander, duel, explorer, future, gladiator, historic, legacy, modern,
oathbreaker, oldschool, pauper, paupercommander, penny, pioneer, predh, premodern, standard,
standardbrawl, timeless, vintage)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
$15, $16, $17, $18, $19, $20, $21, $22, $23) ON CONFLICT DO NOTHING
"""

INSERT_RULE = """
INSERT INTO rule (id, colour_identity, mana_cost, cmc, power, power, toughness, loyalty, defence, type_line, 
oracle_text, colours, keywords, produced_mana)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) ON CONFLICT DO NOTHING
"""

INSERT_SET = "INSERT INTO set (id, name, normalised_name, abbreviation) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING"

INSERT_CARD = """INSERT INTO card 
(id, oracle_id, name, normalised_name, scryfall_url, flavour_text, release_date, reserved, rarity, artist_id, 
image_id, illustration_id, legality_id, rule_id, set_id)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15) ON CONFLICT DO NOTHING
"""

INSERT_TOKEN = "INSERT INTO token (id, name, normalised_name) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING"

INSERT_RELATED_CARD = """
INSERT INTO related_card (id, card_id, related_card_id) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING
"""

INSERT_RELATED_TOKEN = "INSERT INTO related_token (id, card_id, token_id) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING"
