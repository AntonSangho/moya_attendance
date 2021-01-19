##dev_users

create table dev_users
(
    id       int unsigned auto_increment,
    rfid_uid varchar(255)                        not null,
    name     varchar(255)                        not null,
    created  timestamp default CURRENT_TIMESTAMP not null,
    constraint id
        unique (id)
)
    comment '개발용 사용자카드등록';

alter table dev_users
    add primary key (id);

## dev_attendance
create table dev_attendance
(
    id       int unsigned auto_increment,
    user_id  int unsigned                        not null,
    clock_in timestamp default CURRENT_TIMESTAMP not null,
    constraint id
        unique (id)
)
    comment '개발용 출입';

alter table dev_attendance
    add primary key (id);

## dev_exits
create table dev_exits
(
    id       int unsigned auto_increment,
    user_id  int unsigned                        not null,
    clock_in timestamp default CURRENT_TIMESTAMP not null,
    constraint id
        unique (id)
)
    comment '개발용 퇴장';

alter table dev_exits
    add primary key (id);

## dev_user_detail
create table dev_users_detail
(
    id      int unsigned                       not null
        primary key,
    rfid    int                                null,
    name    text                               null,
    sex     text                               null comment '1: 여자
2: 남자
3: 기타',
    phone   varchar(20)                        null comment '연락처',
    year    int                                null comment '태어난년도',
    memo    text                               null comment '추가정보/메모',
    created datetime default CURRENT_TIMESTAMP null,
    constraint dev_users_detail_dev_users__fk
        foreign key (id) references dev_users (id)
)
    comment '개발용사용자상세정보';

create user righthand_dev;

grant SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER on *.* to righthand_dev with grant option;

grant SELECT, INSERT, UPDATE, DELETE on moya.dev_users_detail to righthand_dev;

grant SELECT, INSERT, UPDATE, DELETE on moya.dev_attendance to righthand_dev;

grant SELECT, INSERT, UPDATE, DELETE on moya.dev_exits to righthand_dev;

flush privileges ;

##dev_filter_attendance

create definer = righthand@`%` view dev_filter_attendance as
select `moya`.`dev_attendance`.`user_id`                 AS `user_id`,
       substr(`moya`.`dev_attendance`.`clock_in`, 1, 10) AS `dates`,
       max(`moya`.`dev_attendance`.`clock_in`)           AS `clock_in`
from `moya`.`dev_attendance`
group by `moya`.`dev_attendance`.`user_id`, substr(`moya`.`dev_attendance`.`clock_in`, 1, 10);

## dev_stat_attendance

create definer = righthand@`%` view dev_stat_attendance as
select `a`.`user_id`                                         AS `userid`,
       `a`.`clock_in`                                        AS `entry_time`,
       `b`.`clock_in`                                        AS `exit_time`,
       timestampdiff(MINUTE, `a`.`clock_in`, `b`.`clock_in`) AS `used_time`
from (`moya`.`dev_filter_attendance` `a`
         left join `moya`.`dev_exits` `b` on (((`a`.`user_id` = `b`.`user_id`) and
                                              (substr(`a`.`clock_in`, 1, 10) = substr(`b`.`clock_in`, 1, 10)))))
where ((1 = 1) and (`a`.`clock_in` < `b`.`clock_in`))
order by `a`.`clock_in` desc;