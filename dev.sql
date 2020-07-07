select * from users u
left join users_detail d
on u.id = d.id;

/*
insert 2개의 테이블에서 일어나야 하고

user 테이블에 먼저 들어가 있고

userdetail 에는 user 테이블의 id 가 키로 해서 추가정보가 들어가면 됩니다.
 */

insert into users(id, rfid_uid, name) value
('?', '?', '?');
insert into users()

insert into users_detail(id, sex, phone, age, memo) value
    (1, 2, 'xxx-xxxx-xxxx', 34, '모야');
insert into users_detail(id, sex, phone, age, memo) value
(2, 2, 'xxx-xxxx-xxxx', 37, '비커');

commit;

delete from users_detail;

commit;

-- update
update users
set name = '모야'
where id = 1;

rollback;


update users
set name = '비커'
where id = 2;

commit;

-- append 쿼
update users_detail a, users_detail d
set a.memo = concat(d.memo , ', 추가하는 메모 안녕하세요. 추가입니다.')
where a.id = d.id
and d.id = 1;

commit;


select concat(memo , ', 추가하는 메모')
from users_detail where id = 2;


delete from users
where id = 2;

commit;

delete from users_detail
where id = 2;



