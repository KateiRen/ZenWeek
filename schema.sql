DROP TABLE IF EXISTS tasks;

CREATE TABLE "tasks" (
	"id"	INTEGER NOT NULL UNIQUE,
	"create_date"	TEXT NOT NULL,
	"resolve_date"	TEXT ,
	"taskname"	TEXT NOT NULL,
	"description"	TEXT,
	"url"	TEXT,
	"status"	TEXT NOT NULL,
	"priority"	INTEGER NOT NULL,
	"position"	INTEGER NOT NULL,
	"year"	INTEGER NOT NULL,
	"week"	INTEGER NOT NULL,
	"date"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);