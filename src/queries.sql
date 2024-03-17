
DROP TABLE IF EXISTS vacancies;
DROP TABLE IF EXISTS employers;

CREATE TABLE employers (
    id          int PRIMARY KEY,
    name        varchar,
    description text
);

CREATE TABLE vacancies (
    id              int PRIMARY KEY,
    employer_id     int REFERENCES employers(id),
    name            varchar,
    requirement     text,
    responsibility  text,
    salary_from     int,
    url             varchar(50)
)