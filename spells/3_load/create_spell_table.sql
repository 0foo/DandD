DROP TABLE spells; 

CREATE TABLE spells (
    id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    source TEXT NOT NULL,
    level INTEGER NOT NULL,
    school TEXT NOT NULL,
    ritual TEXT NOT NULL,
    casttime TEXT NOT NULL,
    actiontype TEXT NOT NULL,
    the_range TEXT NOT NULL,
    components TEXT NOT NULL,
    duration TEXT NOT NULL,
    spelllists TEXT NOT NULL,
    description TEXT NOT NULL
);