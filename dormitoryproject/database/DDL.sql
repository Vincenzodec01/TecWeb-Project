create table promotion
(
    id_promotion     int auto_increment
        primary key,
    promotion_name   varchar(20) null,
    p_start_date     datetime    null,
    p_end_date       datetime    null,
    percent_discount int         null
);

create table room_type
(
    id_type     int auto_increment
        primary key,
    name_type   varchar(20)  not null,
    adults      int          not null,
    price       float        not null,
    description varchar(400) not null
);

create table apply_promotion
(
    id_promotion int not null,
    id_type      int not null,
    primary key (id_promotion, id_type),
    constraint FK_promotion_id
        foreign key (id_promotion) references promotion (id_promotion)
            on delete cascade,
    constraint FK_promotion_name_type
        foreign key (id_type) references room_type (id_type)
            on delete cascade
);

create table room
(
    room_number char(3) not null
        primary key,
    id_type     int     not null,
    constraint FK_id_room_type
        foreign key (id_type) references room_type (id_type)
            on delete cascade
);

create table reservation
(
    id_reservation   int auto_increment
        primary key,
    check_in_date    datetime not null,
    check_out_date   datetime not null,
    reservation_date datetime not null,
    start_date       datetime null,
    end_date         datetime null,
    id_type          int      null,
    room_number      char(3)  null,
    cancelled        int      null,
    constraint FK_book_id_type
        foreign key (id_type) references room_type (id_type)
            on delete set null,
    constraint FK_book_room_number
        foreign key (room_number) references room (room_number)
            on delete set null
);

create table payment
(
    id_payment     int auto_increment
        primary key,
    receipt_number char(6)   null,
    total          float     not null,
    payment_date   timestamp not null,
    id_reservation int       null,
    constraint FK_payment_id_reservation
        foreign key (id_reservation) references reservation (id_reservation)
            on delete set null
);

create table review
(
    review_id      int          not null
        primary key,
    vote           int          not null,
    title          varchar(20)  null,
    description    varchar(400) null,
    review_date    timestamp    null,
    id_reservation int          null,
    constraint FK_review_id_reservation
        foreign key (id_reservation) references reservation (id_reservation)
            on delete set null
);

create table staff
(
    id_staff      int auto_increment
        primary key,
    s_fiscal_code char(16)    null,
    s_password    varchar(64) not null,
    s_name        varchar(20) null,
    s_surname     varchar(20) null,
    s_email       varchar(50) null,
    s_gender      char        null,
    role          varchar(15) not null,
    phone         varchar(10) not null,
    secret_key    char(32)    not null,
    access        int         not null,
    constraint s_email
        unique (s_email),
    constraint s_fiscal_code
        unique (s_fiscal_code)
);

create table avatar_staff
(
    id_avatar   int auto_increment primary key,
    name_avatar varchar(100) not null,
    id_user     int          not null,
    constraint FK_id_user_staff_avatar
        foreign key (id_user) references staff (id_staff) on delete cascade
);

create table cleaning
(
    cleaning_id   int auto_increment
        primary key,
    cleaning_date timestamp not null,
    room_number   char(3)   not null,
    id_staff      int       null,
    constraint FK_cleaning_room
        foreign key (room_number) references room (room_number)
            on delete cascade,
    constraint FK_cleaning_staff_id
        foreign key (id_staff) references staff (id_staff)
            on delete set null
);

create table news
(
    id_news          int auto_increment
        primary key,
    title            varchar(20)  not null,
    publication_date datetime     not null,
    description      varchar(400) not null,
    id_staff         int          null,
    constraint FK_news_id_staff
        foreign key (id_staff) references staff (id_staff)
            on delete set null
);

create table user
(
    id_user              int         not null auto_increment
        primary key,
    matriculation_number char(10)    not null,
    email                varchar(20) null,
    fiscal_code          char(16)    not null,
    password             varchar(64) not null,
    name                 varchar(20) not null,
    surname              varchar(20) not null,
    gender               char        null,
    role                 varchar(20) null,
    constraint email
        unique (email),
    constraint fiscal_code
        unique (fiscal_code),
    constraint matriculation_number
        unique (matriculation_number)
);

create table avatar_user
(
    id_avatar   int auto_increment primary key,
    name_avatar varchar(100) not null,
    id_user     int          not null,
    constraint FK_avatar_id_user
        foreign key (id_user) references user (id_user) on delete cascade
);

create table payment_method
(
    number_card char(16)    not null,
    id_user     int         not null,
    exp         char(5)     null,
    name        varchar(30) null,
    cvc         char(3)     not null,
    type        varchar(15) not null,
    primary key (number_card, id_user),
    constraint FK_payment_method_id_user
        foreign key (id_user) references user (id_user)
            on delete cascade
);

create table reservation_user
(
    id_user        int not null,
    id_reservation int not null,
    primary key (id_reservation, id_user),
    constraint FK_book_user
        foreign key (id_user) references user (id_user)
            on delete cascade,
    constraint FK_reservation
        foreign key (id_reservation) references reservation (id_reservation)
            on delete cascade
);

