explain analyse
select front.id as front_id,
       front.name as front_name,
       front.normalised_name as front_normalised_name,
       front_image.png as front_png,
       back.id as back_id,
       back.name as back_name,
       back_image.png as back_png,
       front.release_date as release_date
from card front
         left join related_card on related_card.card_id = front.id
         left join card back on related_card_id = back.id
         left join image front_image on front.image_id = front_image.id
         left join image back_image on back.image_id = back_image.id
where word_similarity(front.normalised_name, 'noble hi') > 0.50
order by front.release_date desc;


SELECT * from card order by random() limit 1;

explain analyse select front_name, back_name, front_normalised_name, front_png, back_id, back_png, release_date from mv_front_back_cards where word_similarity(front_normalised_name, 'noble hi') > 0.50;

create materialized view mv_front_back_cards as
    select front.id as front_id,
       front.name as front_name,
       front.normalised_name as front_normalised_name,
       front_image.png as front_png,
       back.id as back_id,
       back.name as back_name,
       back_image.png as back_png,
       front.release_date as release_date
from card front
         left join related_card on related_card.card_id = front.id
         left join card back on related_card_id = back.id
         left join image front_image on front.image_id = front_image.id
         left join image back_image on back.image_id = back_image.id
order by front.release_date desc;


create index ix_mv_front_normalised_name
    on mv_front_back_cards (front_normalised_name);

create index ix_mv_multi_index
    on mv_front_back_cards (front_name, back_name, front_normalised_name, front_png, back_id, back_png, release_date);


ALTER TABLE mv_front_back_cards SET (parallel_workers = 16, min_parallel_table_scan_size=100);