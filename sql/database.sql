CREATE EXTENSION IF NOT EXISTS dblink;

CREATE OR REPLACE FUNCTION create_database(dbname text, _user text, _password text) RETURNS VOID AS $$
BEGIN
		IF EXISTS (SELECT 1 FROM pg_database WHERE datname = dbname) THEN
			RAISE EXCEPTION 'Database already exists';
		ELSE
			PERFORM dblink_connect('host=localhost user=' || _user ||
			 ' password=' || _password || ' dbname=' || current_database());
			PERFORM dblink_exec('CREATE DATABASE '|| dbname);
		END IF;

	DROP TABLE IF EXISTS purchase CASCADE;
	DROP TABLE IF EXISTS book CASCADE;
	DROP TABLE IF EXISTS person CASCADE;
	

	CREATE TABLE IF NOT EXISTS book (
		book_id SERIAL PRIMARY KEY,
		title VARCHAR NOT NULL UNIQUE,
		author VARCHAR NOT NULL,
		price integer NOT NULL CONSTRAINT valid_price CHECK (price > 0),
		amount integer NOT NULL CONSTRAINT valid_amount CHECK (amount >= 0)
		);

	CREATE INDEX ON book(author);

	CREATE TABLE IF NOT EXISTS person (
		person_id SERIAL PRIMARY KEY,
		first_name VARCHAR NOT NULL,
		last_name VARCHAR NOT NULL,
		patronymic VARCHAR NOT NULL,
		discount integer DEFAULT 0 CONSTRAINT valid_discount CHECK (discount >= 0 AND discount <= 100)
		);

	CREATE INDEX ON person(last_name);

	CREATE TABLE IF NOT EXISTS purchase (
		id SERIAL PRIMARY KEY,
		book_id integer NOT NULL,
		person_id integer NOT NULL,
		dd integer NOT NULL CONSTRAINT valid_dd CHECK (dd >= 1 and dd <= 31),
		mm integer NOT NULL CONSTRAINT valid_mm CHECK (mm >= 1 and mm <= 12),
		purchase_price integer NOT NULL CONSTRAINT valid_price CHECK (purchase_price > 0),
		FOREIGN KEY (book_id) REFERENCES book(book_id)
		ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY (person_id) REFERENCES person(person_id)
		ON DELETE CASCADE ON UPDATE CASCADE
		);
		
	CREATE INDEX ON purchase(book_id);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_database(dbname text, _user text, _password text) RETURNS VOID AS $$
BEGIN
		PERFORM dblink_connect('host=localhost user=' || _user ||
			' password=' || _password || ' dbname=' || current_database());
			PERFORM dblink_exec('DROP DATABASE '|| dbname);
END;
$$ LANGUAGE plpgsql;
