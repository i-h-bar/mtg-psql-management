UPSERT = """
         INSERT INTO price (id, card_id, usd, usd_foil, usd_etched, euro, euro_foil, tix)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
         ON CONFLICT (card_id) DO UPDATE SET usd        = EXCLUDED.usd,
                                             usd_foil   = EXCLUDED.usd_foil,
                                             usd_etched = EXCLUDED.usd_etched,
                                             euro       = EXCLUDED.euro,
                                             euro_foil  = EXCLUDED.euro_foil,
                                             tix        = EXCLUDED.tix;
         """
