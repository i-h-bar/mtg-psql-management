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
oracle_text, colours, keywords, produced_mana, rulings_url) 
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14) ON CONFLICT DO NOTHING
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
            select set.id                 as set_id,
                   front.id               as front_id,
                   front.name             as front_name,
                   front.normalised_name  as front_normalised_name,
                   front.image_id         as front_image_id
                   front_rule.mana_cost   as front_mana_cost,
                   front_rule.power       as front_power,
                   front_rule.toughness   as front_toughness,
                   front_rule.loyalty     as front_loyalty,
                   front_rule.defence     as front_defence,
                   front_rule.type_line   as front_type_line,
                   front_rule.keywords    as front_keywords,
                   front_rule.oracle_text as front_oracle_text,
            
                   back.id                as back_id,
                   back.name              as back_name,
                   back.image_id          as back_image_id
                   back_rule.mana_cost    as back_mana_cost,
                   back_rule.power        as back_power,
                   back_rule.toughness    as back_toughness,
                   back_rule.loyalty      as back_loyalty,
                   back_rule.defence      as back_defence,
                   back_rule.type_line    as back_type_line,
                   back_rule.keywords     as back_keywords,
                   back_rule.oracle_text  as back_oracle_text,
            
                   front.release_date     as release_date
            from card front
                     left join card back on front.backside_id = back.id
                     left join rule front_rule on front.rule_id = front_rule.id
                     left join rule back_rule on back.rule_id = back_rule.id
                     join set on front.set_id = set.id
            where set.normalised_name = '{normalised_name}';
        """

CREATE_ARTIST_MV = """
        create materialized view artist_{artist} as
            select artist.id              as artist_id,
                   front.id               as front_id,
                   front.name             as front_name,
                   front.normalised_name  as front_normalised_name,
                   front_rule.mana_cost   as front_mana_cost,
                   front_rule.power       as front_power,
                   front_rule.toughness   as front_toughness,
                   front_rule.loyalty     as front_loyalty,
                   front_rule.defence     as front_defence,
                   front_rule.type_line   as front_type_line,
                   front_rule.keywords    as front_keywords,
                   front_rule.oracle_text as front_oracle_text,
            
                   back.id                as back_id,
                   back.name              as back_name,
                   back_rule.mana_cost    as back_mana_cost,
                   back_rule.power        as back_power,
                   back_rule.toughness    as back_toughness,
                   back_rule.loyalty      as back_loyalty,
                   back_rule.defence      as back_defence,
                   back_rule.type_line    as back_type_line,
                   back_rule.keywords     as back_keywords,
                   back_rule.oracle_text  as back_oracle_text,
            
                   front.release_date     as release_date
            from card front
                     left join card back on front.backside_id = back.id
                     left join rule front_rule on front.rule_id = front_rule.id
                     left join rule back_rule on back.rule_id = back_rule.id
                     join artist on front.artist_id = artist.id
            where artist.normalised_name = '{normalised_name}';
"""
