create user righthand_01@'%' identified by '1cl1kc02,!c';

select * from mysql.user;

grant select, insert, update  on moya.users to righthand_01@'%';

flush privileges ;


create table jc_exits
select * from exits where 1 = 2;


select * from jc_attendance;

delete from jc_attendance;
commit;;


create table jc_users_detail
select * from users_detail where 1 = 2;

create table jc_users
select * from users where 1 = 2;

grant select, insert, update, delete  on moya.jc_users
    to righthand_01@'%';

revoke select, insert, update on moya.users FROM righthand_01@'%';

create definer = righthand_01@'%' view mh_filter_attendance as
select `moya`.`mh_attendance`.`user_id`                 AS `user_id`,
       substr(`moya`.`mh_attendance`.`clock_in`, 1, 10) AS `dates`,
       max(`moya`.`mh_attendance`.`clock_in`)           AS `clock_in`
from `moya`.`mh_attendance`
group by `moya`.`mh_attendance`.`user_id`, substr(`moya`.`mh_attendance`.`clock_in`, 1, 10);

create definer = righthand_01@`%` view mh_stat_attendance as
select `a`.`user_id`                                         AS `userid`,
       `a`.`clock_in`                                        AS `entry_time`,
       `b`.`clock_in`                                        AS `exit_time`,
       timestampdiff(MINUTE, `a`.`clock_in`, `b`.`clock_in`) AS `used_time`
from (`moya`.`filter_attendance` `a`
         left join `moya`.`exits` `b` on (((`a`.`user_id` = `b`.`user_id`) and
                                           (substr(`a`.`clock_in`, 1, 10) = substr(`b`.`clock_in`, 1, 10)))))
where ((1 = 1) and (`a`.`clock_in` < `b`.`clock_in`))
order by `a`.`clock_in` desc;