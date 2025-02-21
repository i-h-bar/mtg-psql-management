select front.id              as front_id,
       front.name            as front_name,
       front.normalised_name as front_normalised_name,
       front_image.png       as front_png,
       back.id               as back_id,
       back.name             as back_name,
       back_image.png        as back_png,
       front.release_date    as release_date
from card front
         left join card back on front.backside_id = back.id
         left join image front_image on front.image_id = front_image.id
         left join image back_image on back.image_id = back_image.id
where word_similarity(front.normalised_name, 'invation of zendikar') > 0.50
order by front.release_date desc
limit 50;


create materialized view distinct_cards as
    select distinct on (front.name) front.id              as front_id,
                                    front.name            as front_name,
                                    front.normalised_name as front_normalised_name,
                                    front_image.png       as front_png,
                                    back.id               as back_id,
                                    back.name             as back_name,
                                    back_image.png        as back_png,
                                    front.release_date    as release_date
    from card front
             left join card back on front.backside_id = back.id
             left join image front_image on front.image_id = front_image.id
             left join image back_image on back.image_id = back_image.id
    order by front.name, front.release_date desc;


select front_id,
       front_name,
       front_normalised_name,
       front_png,
       back_id,
       back_name,
       back_png,
       release_date
from distinct_cards
where word_similarity(front_normalised_name, 'noble hi') > 0.50;
