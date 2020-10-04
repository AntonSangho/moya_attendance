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
