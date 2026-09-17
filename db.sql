-- ================================================
--   HUNT THE WUMPUS — Script SQL (PostgreSQL)
-- ================================================

CREATE SEQUENCE joueurs_id_seq;

CREATE TABLE userse (
    id           INTEGER      NOT NULL DEFAULT nextval('joueurs_id_seq'),
    pseudo       VARCHAR(255) NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    avatar       VARCHAR(50),
    nbvictory    INTEGER      NOT NULL DEFAULT 0,

    CONSTRAINT users_pkey   PRIMARY KEY (id),
    CONSTRAINT users_pseudo UNIQUE (pseudo)
);

ALTER SEQUENCE joueurs_id_seq OWNED BY users.id;