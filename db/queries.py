INSERT_ARTIST = "INSERT into artist (id, name, normalised_name) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING"

INSERT_ILLUSTRATION = "INSERT into illustration (id, scryfall_url) VALUES ($1, $2) ON CONFLICT DO NOTHING"

INSERT_IMAGE = "INSERT into image (id, scryfall_url) VALUES ($1, $2) ON CONFLICT DO NOTHING"

INSERT_LEGALITY = """
INSERT INTO legality
(id, alchemy, brawl, commander, duel, explorer, future, gladiator, historic, legacy, modern,
oathbreaker, oldschool, pauper, paupercommander, penny, pioneer, predh, premodern, standard,
standardbrawl, timeless, vintage, game_changer)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
$15, $16, $17, $18, $19, $20, $21, $22, $23, $24) ON CONFLICT DO NOTHING
"""

INSERT_RULE = """
INSERT INTO rule (id, colour_identity, mana_cost, cmc, power, toughness, loyalty, defence, type_line, 
oracle_text, colours, keywords, produced_mana)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) ON CONFLICT DO NOTHING
"""

INSERT_SET = "INSERT INTO set (id, name, normalised_name, abbreviation) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING"

INSERT_CARD = """INSERT INTO card 
(id, oracle_id, name, normalised_name, scryfall_url, flavour_text, release_date, reserved, rarity, artist_id, 
image_id, illustration_id, legality_id, rule_id, set_id, backside_id)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16) ON CONFLICT DO NOTHING
"""

INSERT_RELATED_TOKEN = "INSERT INTO related_token (id, card_id, token_id) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING"

INSERT_COMBO = "INSERT INTO combo (id, card_id, combo_card_id) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING"

CREATE_SET_MV = """
        create materialized view set_{set} as
            select front.id                     as front_id,
                   front.name                   as front_name,
                   front.normalised_name        as front_normalised_name,
                   front_image.scryfall_url     as front_scryfall_url,
                   back.id                      as back_id,
                   back.name                    as back_name,
                   back_image.scryfall_url      as back_scryfall_url,
                   front.release_date           as release_date
            from card front
                     left join card back on front.backside_id = back.id
                     left join image front_image on front.image_id = front_image.id
                     left join image back_image on back.image_id = back_image.id
                     join set on front.set_id = set.id
            where set.normalised_name = '{normalised_name}'
        """

CREATE_ARTIST_MV = """
        create materialized view artist_{artist} as
            select front.id                     as front_id,
                   front.name                   as front_name,
                   front.normalised_name        as front_normalised_name,
                   front_image.scryfall_url     as front_scryfall_url,
                   back.id                      as back_id,
                   back.name                    as back_name,
                   back_image.scryfall_url      as back_scryfall_url,
                   front.release_date           as release_date
            from card front
                     left join card back on front.backside_id = back.id
                     left join image front_image on front.image_id = front_image.id
                     left join image back_image on back.image_id = back_image.id
                     join artist on front.artist_id = artist.id
        where artist.normalised_name = '{normalised_name}';
"""
