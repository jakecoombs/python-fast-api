CREATE TABLE posts
(
    id SERIAL NOT NULL,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    published boolean NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT posts_pkey PRIMARY KEY (id)
);

INSERT INTO posts (title, content) VALUES
    ('FIRST POST', 'Some content'),
    ('Another post', 'even more content!'),
    ('Another post', 'even more content!'),
    ('Another post', 'even more content!'),
    ('Another post', 'even more content!'),
    ('Another post', 'even more content!');