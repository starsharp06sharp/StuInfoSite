create table if not exists Users (
    username varchar(255) primary key,
    password char(32) not null
);

create table if not exists Students (
    id varchar(32) primary key,
    name varchar(255) not null,
    gender char(3) not null,
    phonenum varchar(32),
    emailaddr varchar(255),
    check(gender in ('男', '女'))
);