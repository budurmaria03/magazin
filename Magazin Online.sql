drop database Magazin;
create database Magazin;
use Magazin;

create table Produse(
	Id_produs int not null auto_increment primary key,
    Nume varchar(100) not null,
    Pret decimal(10,2) not null,
    Stoc int not null,
    Gramaj int not null,
    Data_fabricatiei date not null,
    Data_expirarii date not  null,
    Categorie int,
    constraint ck_pret check (Pret>=0),
    constraint ck_stoc check (Stoc>=0),
    constraint ck_produs unique (Nume),
    constraint ck_expiration_date check (Data_expirarii>Data_fabricatiei)
);

create table Categorii(
	Id_categorie int not null auto_increment primary key,
	Nume varchar(50) not null unique
);

create table Clienti(
	Id_client int not null auto_increment primary key,
    Nume varchar(100) not null,
    Prenume varchar(100) not null,
    Email varchar(100) not null unique,
    Telefon varchar(20) not null,
    Adresa varchar(255) not null,
    constraint ck_telefon_format check (Telefon regexp '^[0-9]+$')
);

create table Comenzi(
	Id_comanda int not null auto_increment primary key unique,
    Data_comenzii date not null,
    Clienti int,
    Angajat int
);

create table Detalii_comanda(
	Id_detaliu int not null auto_increment primary key,
    Cantitate int not null,
    Produs int,
    Comanda int,
    constraint ck_cantitate check (Cantitate>0)
);

create table Angajati(
	Id_angajat int not null auto_increment primary key,
    Nume varchar(100) not null,
    Prenume varchar(100) not null,
    Salariu decimal(10,2) not null default '2500',
    Functie varchar(100) not null
);

alter table produse add constraint categorie_produs foreign key (Categorie) references categorii(Id_categorie);
alter table comenzi add constraint client_comanda foreign key (Clienti) references clienti(Id_client);
alter table comenzi add constraint angajat_comanda foreign key (Angajat) references angajati(Id_angajat);
alter table detalii_comanda add constraint produs_detaliu foreign key (Produs) references produse(Id_produs);
alter table detalii_comanda add constraint comanda_detaliu foreign key (Comanda) references comenzi(Id_comanda);

/*select * from produse inner join categorii on produse.Id_produs=categorii.Id_categorie;
select * from comenzi inner join clienti on comenzi.Id_comanda=clienti.Id_client;
select * from comenzi inner join categorii on produse.Id_produs=categorii.Id_categorie;
select * from detalii_comanda inner join comenzi on detalii_comanda.Id_detaliu=comenzi.Id_comanda;
select * from detalii_comanda inner join produse on detalii_comanda.Id_detaliu=produse.Id_produs;*/

insert into categorii (Nume) values ('brutarie');
insert into categorii (Nume) values ('suc');

INSERT INTO Produse (Nume, Pret, Stoc, Gramaj, Data_fabricatiei, Data_expirarii, Categorie) VALUES ('paine',3,20,300,'2021-12-02','2021-12-05',1);
INSERT INTO Produse (Nume, Pret, Stoc, Gramaj, Data_fabricatiei, Data_expirarii, Categorie) VALUES ('fanta',3,12,30,'2021-11-02','2021-12-05',2);
INSERT INTO Produse (Nume, Pret, Stoc, Gramaj, Data_fabricatiei, Data_expirarii, Categorie) VALUES ('sprite',12,12,30,'2021-11-02','2021-12-05',2);

select * from produse;
select * from categorii;
