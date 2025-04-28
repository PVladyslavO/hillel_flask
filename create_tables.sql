CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date DATE NOT NULL,
    course_name TEXT,
    photo_url TEXT
);
INSERT INTO students (name, birth_date) VALUES ('John Doe', '2000-01-01');