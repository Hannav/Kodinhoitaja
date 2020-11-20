## Käyttötapaukset ja niihin liittyvät SQL-kyselyt

Käyttötapaukset | SQL-kyselyt
----------------|------------
Käyttäjätunnuksen luominen|INSERT INTO account (name, username, password) VALUES (:username, :username, :password)
Sisäänkirjautuminen|SELECT account.id AS account_id, account.date_created AS account_date_created, account.date_modified AS account_date_modified, account.name AS account_name, account.username AS account_username, account.password AS account_password FROM account WHERE account.username = :username AND account.password = :password
Lisää matka|INSERT INTO trip (date_created, date_modified, name, owner_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, :name, :current_user_id)
Poista matka|DELETE FROM trip WHERE trip.id = :trip_id
Lisää osallistuja|INSERT INTO trip_participant (date_created, date_modified, participant_id, trip_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, :participant_id, :trip_id)
Poista osallistuja|DELETE FROM trip_participant WHERE (id = :id)
Lisää pakattava|INSERT INTO task (date_created, date_modified, name, done, packer_id, trip_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, :name, :done, :current_user_id, :trip_id)
Muokkaa pakattavan nimeä|UPDATE item SET name = (:name) WHERE (id = :id)
Merkitse pakatuksi (Muuta status-painike)|UPDATE item SET done = True WHERE (id = :id)
Merkitse pakkaamattomaksi (Muuta status-painike)|UPDATE item SET done = False WHERE (id = :id)
Poista pakattava|DELETE FROM item WHERE (id = :id)
Matkat-listaus|SELECT trip.id AS trip_id, trip.date_created AS trip_date_created, trip.date_modified AS trip_date_modified, trip.name AS trip_name, trip.owner_id AS trip_owner_id FROM trip WHERE trip.owner_id = :current_user_id OR (EXISTS (SELECT 1 FROM trip_participant WHERE trip.id = trip_participant.trip_id AND trip_participant.participant_id = :current_user_id)) ORDER BY trip.date_modified DESC
Matkakohtainen Pakattavat-listaus (matka valittu Matkat-listauksesta)|SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.done AS task_done, task.packer_id AS task_packer_id, task.trip_id AS task_trip_id FROM task WHERE task.trip_id = :trip_id
Matkakohtainen Osallistujat-listaus (matka valittu Matkat-listauksesta)|SELECT trip_participant.id AS trip_participant_id, trip_participant.date_created AS trip_participant_date_created, trip_participant.date_modified AS trip_participant_date_modified, trip_participant.participant_id AS trip_participant_participant_id, trip_participant.trip_id AS trip_participant_trip_id FROM trip_participant WHERE trip_participant.trip_id = :trip_id
