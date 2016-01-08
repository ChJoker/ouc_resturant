create table Rtable(
	Tid int not null primary key identity(1,1),
	Tsize int not null,
	Tstate int,
	Tname nvarchar(32)
);


create table bill(
	Bid int not null primary key identity(1,1),
	Bsun float ,
	Bdate nvarchar(64), 
	Bstate int
);

create table Sort(
	Soid int not null primary key identity(1,1),
	Sname nvarchar(64)
);

create table dish(
	Did int not null primary key identity(1,1),
	Soid int foreign key references Sort(Soid),
	Dname nvarchar(64),
	Dpice float,
	Dpic nvarchar(256)
);

create table Cook(
	Cid int not null primary key identity(1,1),
	Cnum nvarchar(16),
	Soid int foreign key references Sort(Soid),
	Cname nvarchar(64),
	Cage int,
	Csex nvarchar(8)
);
create table B_D_T (
	id int not null primary key identity(1,1),
	Bid int foreign key references Bill(Bid),
	Did int foreign key references Dish(Did),
	Tid int foreign key references Rtable(Tid),
	Cid int foreign key references Cook(Cid),
	Bdate nvarchar(64), 
	nstate int
);


create table Waiter(
	Wid int not null primary key identity(1,1),
	Wnum nvarchar(16),	
	Wname nvarchar(64),
	Wage int,
	wsex nvarchar(8),
	Wroom nvarchar(64)
);


if (object_id('waiter_num', 'tr') is not null)
    drop trigger waiter_num
go
create trigger waiter_num
on Waiter
after insert
as
update Waiter set Wnum= CONVERT(VARCHAR(32), GETDATE(), 112)+ REPLACE(STR(inserted.Wid%100, 2, 0), ' ', '0')
from Waiter,inserted
where
Waiter.Wid=inserted.Wid
go
if (object_id('cook_num', 'tr') is not null)
    drop trigger cook_num
go
create trigger cook_num
on Cook
after insert
as
update Cook set Cnum= CONVERT(VARCHAR(32), GETDATE(), 112)+ REPLACE(STR(inserted.Cid%100, 2, 0), ' ', '0')
from Cook,inserted
where
Cook.Cid=inserted.Cid
go
if (object_id('bill_date', 'tr') is not null)
    drop trigger bill_date
go
create trigger bill_date
on bill
after insert
as
update bill set Bdate= CONVERT(VARCHAR(64), GETDATE(), 20)
from bill,inserted
where
bill.Bid=inserted.Bid

go
if (object_id('dish_date', 'tr') is not null)
    drop trigger dish_date
go
create trigger dish_date
on B_D_T
after insert
as
update B_D_T set Bdate= CONVERT(VARCHAR(64), GETDATE(), 20)
from B_D_T,inserted
where
B_D_T.id=inserted.id