CREATE TABLE IF NOT EXISTS Migrations (
    id          SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Messages (
    id          BIGINT NOT NULL PRIMARY KEY,
    channel_id  BIGINT NOT NULL,
    cat_id      BIGINT,
    guild_id    BIGINT NOT NULL,
    author_id   BIGINT NOT NULL,
    staff       BOOLEAN NOT NULL,
    bot         BOOLEAN NOT NULL,
    created_at  TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS DeletedMessages (
    id          BIGINT NOT NULL PRIMARY KEY,
    deleted_at  TIMESTAMP NOT NULL
);
