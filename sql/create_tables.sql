create table set
(
    id              uuid primary key,
    name            text,
    normalised_name text,
    abbreviation    text
);

create table image
(
    id           uuid primary key,
    scryfall_url text
);


create table illustration
(
    id           uuid primary key,
    scryfall_url text
);

create table artist
(
    id              uuid primary key,
    name            text,
    normalised_name text
);


create table legality
(
    id              uuid primary key,
    alchemy         text,
    brawl           text,
    commander       text,
    duel            text,
    future          text,
    gladiator       text,
    historic        text,
    legacy          text,
    modern          text,
    oathbreaker     text,
    oldschool       text,
    pauper          text,
    paupercommander text,
    penny           text,
    pioneer         text,
    predh           text,
    premodern       text,
    standard        text,
    standardbrawl   text,
    timeless        text,
    vintage         text,
    game_changer    bool
);


create table rule
(
    id              uuid primary key,
    colour_identity char(1)[],
    mana_cost       text,
    cmc             integer,
    power           text,
    toughness       text,
    loyalty         text,
    defence         text,
    type_line       text,
    oracle_text     text,
    colours         char(1)[],
    keywords        text[],
    produced_mana   char(1)[],
    rulings_url     text
);


create table card
(
    id              uuid primary key,
    oracle_id       uuid,
    name            text,
    normalised_name text,
    scryfall_url    text,
    flavour_text    text,
    release_date    date,
    reserved        bool,
    rarity          text,
    artist_id       uuid references artist (id),
    image_id        uuid references image (id),
    illustration_id uuid references illustration (id),
    set_id          uuid references set (id),
    backside_id     uuid,
    foreign key (oracle_id) references legality (id),
    foreign key (oracle_id) references rule (id)
);


create table related_token
(
    id       uuid primary key,
    card_id  uuid references card (id),
    token_id uuid references card (id)
);


create table combo
(
    id            uuid primary key,
    card_id       uuid references card (id),
    combo_card_id uuid references card (id)
);

create table price
(
    id           uuid primary key references card (id),
    usd          decimal(10, 2),
    usd_foil     decimal(10, 2),
    usd_etched   decimal(10, 2),
    euro         decimal(10, 2),
    euro_foil    decimal(10, 2),
    tix          decimal(10, 2),
    updated_time time with time zone
);
