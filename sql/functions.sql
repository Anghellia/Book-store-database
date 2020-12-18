-- ADD --

DROP FUNCTION IF EXISTS add_new_book(VARCHAR, VARCHAR, integer, integer);
CREATE OR REPLACE FUNCTION add_new_book(title VARCHAR, author VARCHAR, price integer, amount integer) RETURNS VOID AS $$
BEGIN
    INSERT INTO book(book_id, title, author, price, amount) 
	VALUES (DEFAULT, title, author, price, amount);
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS add_new_person(VARCHAR, VARCHAR, VARCHAR, integer);
CREATE OR REPLACE FUNCTION add_new_person(first_name VARCHAR, last_name VARCHAR, patronymic VARCHAR, discount integer) RETURNS VOID AS $$
BEGIN
    INSERT INTO person(person_id, first_name, last_name, patronymic, discount)
	VALUES (DEFAULT, first_name, last_name, patronymic, discount);
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS add_new_purchase(VARCHAR, VARCHAR, VARCHAR, VARCHAR, integer, integer);
CREATE OR REPLACE FUNCTION add_new_purchase(new_title VARCHAR, new_firstname VARCHAR, new_lastname VARCHAR, new_patronymic VARCHAR,
                              new_dd integer, new_mm integer) RETURNS VOID AS $$
BEGIN
    IF (SELECT COUNT(*) FROM person WHERE first_name = new_firstname 
	                                      AND last_name = new_lastname
										  AND patronymic = new_patronymic) < 1 THEN
	    PERFORM add_new_person(new_firstname, new_lastname, new_patronymic, 0);
	END IF;
	INSERT INTO purchase(id, book_id, person_id, dd, mm, purchase_price) VALUES
        (DEFAULT,
		(SELECT book_id FROM book WHERE title = new_title),
	    (SELECT person_id FROM person WHERE first_name = new_firstname 
		                              AND last_name = new_lastname
									  AND patronymic = new_patronymic),
		new_dd, new_mm,
		(SELECT price FROM book WHERE title = new_title));
END;
$$ LANGUAGE plpgsql;


-- EDIT --

DROP FUNCTION IF EXISTS edit_book_by_title(VARCHAR, integer);
CREATE OR REPLACE FUNCTION edit_book_by_title(new_title VARCHAR, id integer) RETURNS VOID AS $$
BEGIN
    UPDATE book SET title = new_title WHERE book_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS edit_book_by_author(VARCHAR, integer);
CREATE OR REPLACE FUNCTION edit_book_by_author(new_author VARCHAR, id integer) RETURNS VOID AS $$
BEGIN
    UPDATE book SET author = new_author WHERE book_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS edit_book_by_price(integer, integer);
CREATE OR REPLACE FUNCTION edit_book_by_price(new_price integer, id integer) RETURNS VOID AS $$
BEGIN
    UPDATE book SET price = new_price WHERE book_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS edit_book_by_amount(integer, integer);
CREATE OR REPLACE FUNCTION edit_book_by_amount(new_amount integer, id integer) RETURNS VOID AS $$
BEGIN
    UPDATE book SET amount = new_amount WHERE book_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS edit_person_by_firstname(VARCHAR, integer);
CREATE OR REPLACE FUNCTION edit_person_by_firstname(new_firstname VARCHAR, id integer) RETURNS VOID AS $$
BEGIN
    UPDATE person SET first_name = new_firstname WHERE person_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS edit_person_by_lastname(VARCHAR, integer);
CREATE OR REPLACE FUNCTION edit_person_by_lastname(new_lastname VARCHAR, id integer) RETURNS VOID AS $$
BEGIN
    UPDATE person SET last_name = new_lastname WHERE person_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS edit_person_by_patronymic(VARCHAR, integer);
CREATE OR REPLACE FUNCTION edit_person_by_patronymic(new_patronymic VARCHAR, id integer) RETURNS VOID AS $$
BEGIN
    UPDATE person SET patronymic = new_patronymic WHERE person_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS edit_person_by_discount(integer, integer);
CREATE OR REPLACE FUNCTION edit_person_by_discount(new_discount integer, id integer) RETURNS VOID AS $$
BEGIN
    UPDATE person SET discount = new_discount WHERE person_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS edit_purchase_by_day(integer, integer);
CREATE OR REPLACE FUNCTION edit_purchase_by_day(day integer, _id integer) RETURNS VOID AS $$
BEGIN
    UPDATE purchase SET dd = day WHERE id = _id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS edit_purchase_by_month(integer, integer);
CREATE OR REPLACE FUNCTION edit_purchase_by_month(month integer, _id integer) RETURNS VOID AS $$
BEGIN
    UPDATE purchase SET mm = month WHERE id = _id;
END;
$$ LANGUAGE plpgsql;


-- VIEW --

DROP FUNCTION IF EXISTS view_book();
CREATE OR REPLACE FUNCTION view_book() RETURNS SETOF book AS $$
BEGIN
    RETURN QUERY
    SELECT * from book;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS view_person();
CREATE OR REPLACE FUNCTION view_person() RETURNS SETOF person AS $$
BEGIN
    RETURN QUERY
    SELECT * from person;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS view_purchase();
CREATE OR REPLACE FUNCTION view_purchase() RETURNS SETOF purchase AS $$
BEGIN
    RETURN QUERY
    SELECT * from purchase;
END;
$$ LANGUAGE plpgsql;


-- CLEAR TABLES --

DROP FUNCTION IF EXISTS clear_purchase_records();
CREATE OR REPLACE FUNCTION clear_purchase_records() RETURNS VOID AS $$
BEGIN
    TRUNCATE TABLE purchase CASCADE;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS clear_person_records();
CREATE OR REPLACE FUNCTION clear_person_records() RETURNS VOID AS $$
BEGIN
    TRUNCATE TABLE person CASCADE;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS clear_book_records();
CREATE OR REPLACE FUNCTION clear_book_records() RETURNS VOID AS $$
BEGIN
    TRUNCATE TABLE book CASCADE;
END;
$$ LANGUAGE plpgsql;


-- CLEAR ALL TABLES --

DROP FUNCTION IF EXISTS clear_all_records();
CREATE OR REPLACE FUNCTION clear_all_records() RETURNS VOID AS $$
BEGIN
    PERFORM clear_purchase_records();
    PERFORM clear_person_records();
    PERFORM clear_book_records();
END;
$$ LANGUAGE plpgsql;


-- SEARCH BY INDEX --

DROP FUNCTION IF EXISTS search_by_author(VARCHAR);
CREATE OR REPLACE FUNCTION search_by_author(author_to_search VARCHAR) RETURNS SETOF book AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM book WHERE author = author_to_search;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS search_by_lastname(VARCHAR);
CREATE OR REPLACE FUNCTION search_by_lastname(lastname_to_search VARCHAR) RETURNS SETOF person AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM person WHERE last_name = lastname_to_search;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS search_by_book_id(integer);
CREATE OR REPLACE FUNCTION search_by_book_id(book_id_to_search integer) RETURNS SETOF purchase AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM purchase WHERE book_id = book_id_to_search;
END;
$$ LANGUAGE plpgsql;


-- DELETE BY INDEX --

DROP FUNCTION IF EXISTS delete_by_author(VARCHAR);
CREATE OR REPLACE FUNCTION delete_by_author(author_to_delete text) RETURNS VOID AS $$
BEGIN
    IF (SELECT COUNT(*) FROM book WHERE author = author_to_delete) = 0
	    THEN RAISE NOTICE 'There are no records with this author in database!';
	ELSE
	    DELETE FROM book WHERE author = author_to_delete;
	END IF;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_by_lastname(VARCHAR);
CREATE OR REPLACE FUNCTION delete_by_lastname(lastname_to_delete VARCHAR) RETURNS VOID AS $$
BEGIN
    IF (SELECT COUNT(*) FROM person WHERE last_name = lastname_to_delete) = 0
	    THEN RAISE NOTICE 'There are no records with this lastname in database!';
	ELSE
	    DELETE FROM person WHERE last_name = lastname_to_delete;
	END IF;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_by_book_id(integer);
CREATE OR REPLACE FUNCTION delete_by_book_id(book_id_to_delete integer) RETURNS VOID AS $$
BEGIN
    IF (SELECT COUNT(*) FROM purchase WHERE book_id = book_id_to_delete) = 0
	    THEN RAISE NOTICE 'There are no records with this book_id in database!';
	ELSE
	    DELETE FROM purchase WHERE book_id = book_id_to_delete;
	END IF;
END;
$$ LANGUAGE plpgsql;


-- DELETE THE RECORD --

DROP FUNCTION IF EXISTS delete_book_record(integer);
CREATE OR REPLACE FUNCTION delete_book_record(id integer) RETURNS VOID AS $$
BEGIN
    DELETE FROM book WHERE book_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_person_record(integer);
CREATE OR REPLACE FUNCTION delete_person_record(id integer) RETURNS VOID AS $$
BEGIN
    DELETE FROM person WHERE person_id = id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_purchase_record(integer);
CREATE OR REPLACE FUNCTION delete_purchase_record(_id integer) RETURNS VOID AS $$
BEGIN
    DELETE FROM purchase WHERE id = _id;
END;
$$ LANGUAGE plpgsql;


-- TRIGGERS --

DROP TRIGGER IF EXISTS buy_book ON book;
DROP TRIGGER IF EXISTS after_insert_purchase ON purchase;

CREATE OR REPLACE FUNCTION buy_book() RETURNS TRIGGER AS $$
BEGIN
	UPDATE book SET amount = amount - 1 WHERE book.book_id = NEW.book_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_insert_purchase AFTER INSERT ON purchase
FOR EACH ROW EXECUTE PROCEDURE buy_book();


DROP TRIGGER IF EXISTS calculate_total_price ON purchase;
DROP TRIGGER IF EXISTS calculate_purchase_price_with_discount ON purchase;

CREATE OR REPLACE FUNCTION calculate_total_price() RETURNS TRIGGER AS $$
BEGIN
    UPDATE purchase SET purchase_price = purchase_price - purchase_price*
	(SELECT discount FROM person WHERE person.person_id = purchase.person_id) / 100;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_purchase_price_with_discount AFTER INSERT ON purchase
FOR EACH ROW EXECUTE PROCEDURE calculate_total_price();


-- STATISTICS --

DROP FUNCTION IF EXISTS get_buy_number_by_month(integer, integer);
CREATE OR REPLACE FUNCTION get_buy_number_by_month(month integer) RETURNS int AS $$
BEGIN
    SELECT COUNT(*) FROM buy WHERE mm = month;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS get_buy_number_by_day(integer, integer);
CREATE OR REPLACE FUNCTION get_buy_number_by_day(day integer, month integer) RETURNS int AS $$
BEGIN
    SELECT COUNT(*) FROM buy WHERE dd = day AND mm = month;
END;
$$ LANGUAGE plpgsql;
