## CREATE TABLE-lauseet

```
CREATE TABLE account (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        username VARCHAR(144) NOT NULL,
        password VARCHAR(144) NOT NULL, PRIMARY KEY (id)
)
```

```
CREATE TABLE trip (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144),
        owner_id INTEGER, PRIMARY KEY (id), FOREIGN KEY(owner_id) REFERENCES account (id)
)
```

```
CREATE TABLE trip_participant (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        participant_id INTEGER,
        trip_id INTEGER, PRIMARY KEY (id), FOREIGN KEY(participant_id) REFERENCES account (id), FOREIGN KEY(trip_id) REFERENCES trip (id)
)
```

```
CREATE TABLE item (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        done BOOLEAN NOT NULL,
        packer_id INTEGER,
        trip_id INTEGER NOT NULL, PRIMARY KEY (id), CHECK (done IN (0, 1)), FOREIGN KEY(packer_id) REFERENCES account (id), FOREIGN KEY(trip_id) REFERENCES trip (id)
)
```
