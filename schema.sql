create table snippets (
keyword text primary key,
message text not null default ''
);

alter table snippets (
hidden boolean not null default false
);
