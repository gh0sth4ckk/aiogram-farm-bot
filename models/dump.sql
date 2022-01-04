CREATE TABLE "users" (
	"id"	INT NOT NULL ,
	"nick"	varchar(255) NOT NULL,
	"level"	INT NOT NULL,
	"points" INT NOT NULL,
	"coins"	INT NOT NULL,
	"wood"	INT NOT NULL,
	"barn_accumulation"	INT NOT NULL,
	PRIMARY KEY("id")
);


CREATE TABLE "buildings" (
	"user_id"	INTEGER NOT NULL,
	"house"	INTEGER NOT NULL,
	"barn"	INTEGER NOT NULL,
	"chicken_coop" INTEGER NOT NULL,
	"cowshed" INTEGER NOT NULL,
	PRIMARY KEY("user_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);



CREATE TABLE "animals" (
	"user_id" INTEGER NOT NULL,
	"sheep" INTEGER NOT NULL,
	"chicken" INTEGER NOT NULL,
	"cow" INTEGER NOT NULL,
	PRIMARY KEY("user_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
)


CREATE TABLE "user_items" (
	"user_id" INTEGER NOT NULL,
	"wool" INT NOT NULL,
	"egg" INT NOT NULL,
	"milk" INT NOT NULL,
	PRIMARY KEY("user_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
)


CREATE TABLE "temp_items" (
	"user_id" INTEGER NOT NULL,
	"wool" INT NOT NULL,
	"egg" INT NOT NULL,
	"milk" INT NOT NULL,
	PRIMARY KEY("user_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
)