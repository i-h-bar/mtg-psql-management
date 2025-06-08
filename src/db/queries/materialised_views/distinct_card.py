CREATE = """
    create materialized view distinct_cards as
        select distinct on (front.name) front.id                     as front_id,
                                        front.name                   as front_name,
                                        front.normalised_name        as front_normalised_name,
                                        front.scryfall_url           as front_scryfall_url,
                                        front.image_id               as front_image_id,
                                        front.illustration_id        as front_illustration_id,
                                        front_rule.mana_cost         as front_mana_cost,
                                        front_rule.colour_identity   as front_colour_identity,
                                        front_rule.power             as front_power,
                                        front_rule.toughness         as front_toughness,
                                        front_rule.loyalty           as front_loyalty,
                                        front_rule.defence           as front_defence,
                                        front_rule.type_line         as front_type_line,
                                        front_rule.keywords          as front_keywords,
                                        front_rule.oracle_text       as front_oracle_text,

                                        back.id                      as back_id,
                                        back.name                    as back_name,
                                        back.scryfall_url            as back_scryfall_url,
                                        back.image_id                as back_image_id,
                                        back.illustration_id         as back_illustration_id,
                                        back_rule.mana_cost          as back_mana_cost,
                                        back_rule.colour_identity    as back_colour_identity,
                                        back_rule.power              as back_power,
                                        back_rule.toughness          as back_toughness,
                                        back_rule.loyalty            as back_loyalty,
                                        back_rule.defence            as back_defence,
                                        back_rule.type_line          as back_type_line,
                                        back_rule.keywords           as back_keywords,
                                        back_rule.oracle_text        as back_oracle_text,

                                        front.release_date           as release_date,
                                        artist.name                  as artist,
                                        set.name                     as set_name
        from card front
                 left join card back on front.backside_id = back.id
                 left join rule front_rule on front.rule_id = front_rule.id
                 left join rule back_rule on back.rule_id = back_rule.id
                 left join artist on front.artist_id = artist.id
                 left join set on set.id = front.set_id
        order by front.name, front.release_date desc;
"""
