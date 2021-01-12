create user 'adminmoya'@'%' identified by 'sangho_2069';

grant SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER on *.* to adminmoya with grant option;

grant SELECT, INSERT, UPDATE, DELETE on moya.attendance to adminmoya;
grant SELECT, INSERT, UPDATE, DELETE on moya.mh_attendance to adminmoya;

grant SELECT, INSERT, UPDATE, DELETE on moya.exits to adminmoya;
grant SELECT, INSERT, UPDATE, DELETE on moya.mh_exits to adminmoya;

grant SELECT, INSERT, UPDATE, DELETE on moya.users_detail to adminmoya;
grant SELECT, INSERT, UPDATE, DELETE on moya.mh_users_detail to adminmoya;

grant ALL PRIVILEGES on moya.exits to adminmoya;
grant ALL PRIVILEGES on moya.mh_exits to adminmoya;

grant SELECT, INSERT, UPDATE, DELETE on moya.users to adminmoya;
grant SELECT, INSERT, UPDATE, DELETE on moya.mh_users to adminmoya;

grant ALL PRIVILEGES on moya.attendance to adminmoya;
grant ALL PRIVILEGES on moya.mh_attendance to adminmoya;

flush privileges ;