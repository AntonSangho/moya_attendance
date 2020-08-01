select  count(*) from exits;

select count(*) from attendance;


create or replace view  filter_attendance as
select distinct user_id, max(clock_in) as clock_in from attendance
-- where substr(clock_in, 1, 10) = '2020-07-31'
group by user_id;

create or replace  view  filter_attendance as
select distinct user_id, substr(clock_in, 1, 10) as dates,
                max(clock_in) as clock_in from attendance
group by user_id, substr(clock_in, 1, 10);



select  * from exits;

select(a.clock_in, 1, 10) ='2020-07-31';

select * from filter_attendance;

create or replace view stat_attentance as
select a.user_id as 'userid',
       a.clock_in as 'entry_time',
       b.clock_in as 'exit_time',
       (b.clock_in - a.clock_in)/3600 as 'used_time'
from
     filter_attendance  a -- 출입
    left join exits b -- 퇴장 있을수도 없을있도 있다
on a.user_id = b.user_id -- 정상적인 출입은 있고 퇴장은 있어도 되고 없어도 되
and substr(a.clock_in, 1, 10) = substr(b.clock_in, 1, 10)
where
      1 = 1
  -- and substr(a.clock_in, 1, 10) ='2020-07-31'
order by a.clock_in desc;
select  userid , substr(entry_time, 1, 10) from stat_attentance;


b.clock_in and b.clock_in;

select substr(clock_in, 1, 10) from attendance a;

select substr(clock_in, 1, 10) from attendance b;


--
select  userid, substr(entry_time, 1, 10), max(used_time) from stat_attentance
where  substr(entry_time, 1, 10) = '2020-08-01' -- 이것만 바꿔치기 하시면 됨
group by  userid, substr(entry_time, 1, 10);
