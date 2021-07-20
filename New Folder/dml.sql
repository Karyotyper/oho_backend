create table user_simpleton
(
	id int,
	email varchar(40)  unique not null,
	name varchar(100) not null,
	phone int not null,
	gender varchar(2) not null,
	occupation varchar(50) not null,
	preferred_gender varchar(2) not null,
	dob date,
	city varchar(50),
	state varchar(50),
	primary key(id)
);