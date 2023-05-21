CREATE TABLE news_source (
    id TEXT PRIMARY KEY, 
    show_name TEXT, 
    source_url TEXT
);

INSERT INTO news_source (id, show_name, source_url) VALUES 
    ('ria', 'РИА Новости', 'https://ria.ru/export/rss2/archive/index.xml'), 
    ('finam_companies', 'Finam.ru - новости компаний', 'https://www.finam.ru/analysis/conews/rsspoint/'), 
    ('investing', 'Investing.com', 'https://ru.investing.com/news/headlines');

CREATE TABLE headline (
    source TEXT REFERENCES news_source,
    link TEXT UNIQUE, 
    title TEXT NOT NULL, 
    release_time TIMESTAMPTZ NOT NULL
);

CREATE TABLE telegram_user (
    id INTEGER PRIMARY KEY, 
    number_of_news INTEGER DEFAULT 5, 
    subscriptions TEXT
);
