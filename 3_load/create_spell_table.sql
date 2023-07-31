CREATE TABLE spells (
    key INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    level INTEGER NOT NULL,
    school TEXT NOT NULL,
    casttime INTEGER  NOT NULL,
    actiontype TEXT NOT NULL,
    the_range TEXT NOT NULL,
    components TEXT NOT NULL,
    duration TEXT NOT NULL,
    description TEXT NOT NULL,
    spelllists TEXT NOT NULL
);