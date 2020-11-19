# Matkapakkaaja
Matkapakkaaja on työkalu yhteisille pakkauslistoille. Käyttäjä voi luoda matkan, jolle lisää osallistujia ja jokainen osallistuja voi lisätä pakattavia tarvikkeita sekä merkitä pakkaamansa pakatuiksi tai pakkaamattomiksi.

[Matkapakkaaja Herokussa](https://matkapakkaaja.herokuapp.com/)

## Asennusohje

Kloonaa ohjelman projekti:

`git clone git@github.com:Hannav/Matkapakkaaja.git`

Mene hakemistoon:

`cd Matkapakkaaja`

Käynnistä virtuaaliympäristö:

`source venv/bin/activate`

Lataa riippuvuudet:

`pip install -r requirements.txt`

Käynnistä ohjelma:

`python run.py`

## Käyttöohje

#### Käyttäjätunnuksen luominen

Paina yläpalkissa "Luo käyttäjätunnus" ja kirjoita kenttiin valitsemasi käyttäjätunnus ja salasana. Paina "Luo käyttäjä".

#### Sisäänkirjautuminen

Paina yläpalkissa "Kirjaudu sisään" ja kirjoita kenttiin käyttäjätunnuksesi ja salasanasi. Paina "Kirjaudu sisään".

#### Lisää matka

Paina Matkat-listauksen alla "Lisää matka"-painiketta. Kirjoita kenttään matkan nimi ja paina "Lisää matka"-painiketta.

#### Poista matka

Valitse Matkat-listauksesta poistettava matka. Paina pakattavien ja osallistujien alapuolella olevaa "Poista matka"-painiketta.

#### Matkat-listaukseen

Paina "Matkapakkaaja" yläpalkin vasemmassa reunassa.

#### Lisää osallistuja

Paina valitsemasi matkan nimeä. Paina Osallistujat-listauksen alla "Lisää osallistuja"-painiketta. Kirjoita kenttään osallistujan nimi. Paina "Lisää osallistuja"-painiketta. 

#### Poista osallistuja

Paina valitsemasi matkan nimeä. Paina Osallistujat-listauksessa poistettavan osallistujan oikealla puolella näkyvää "Poista"-painiketta.

#### Lisää pakattava

Valitse Matkat-listauksesta matka. Paina Pakattava-sarakkeen (ja mahdollisten pakattavaksi listattujen esineiden) alta "Lisää pakattava"-painiketta. Kirjoita kenttään pakattavan esineen nimi. Pakattava on oletusarvoisesti pakkaamaton, mutta halutessasi voit merkitä sen kentän alapuolella olevaan valintaruutuun pakatuksi. Paina "Lisää pakattava".

#### Muokkaa pakattavan nimeä

Valittuasi matkan, näet pakattavien listan. Jokaisen pakattavan kohdalla on oikealla puolella kolme painiketta, joista yksi on "Muokkaa". Paina sitä. Kirjoita pakattavan nimi uudelleen kenttään. Paina "Muokkaa".

#### Merkitse pakatuksi

Valittuasi matkan, näet pakattavien listan. Jokaisen pakattavan kohdalla on oikealla puolella kolme painiketta, joista yksi on "Muuta status". Painamalla sitä, muuttuu Pakattu-sarakkeen arvo pakatusta, True, pakkaamattomaksi, False, tai toisinpäin.

#### Poista pakattava

Valittuasi matkan, näet pakattavien listan. Jokaisen pakattavan kohdalla on oikealla puolella kolme painiketta, joista yksi on "Poista". Painamalla sitä poistat pakattavan.

#### Uloskirjautuminen

Paina yläpalkissa "Kirjaudu ulos".

## Käyttötapaukset ja niihin liittyvät SQL-kyselyt

Käyttötapaukset | SQL-kyselyt
----------------|------------
Käyttäjätunnuksen luominen|x
Sisäänkirjautuminen|

Käyttötapaukset kirjautuneena| SQL-kyselyt
-----------------------------|------------
x | x

## Tietokantarakenteen kuvaus

* [Tietokantakaavio](https://github.com/Hannav/Kodinhoitaja/blob/master/documentation/tietokantakaavio.png)

* CREATE TABLE-lauseet

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
CREATE TABLE task (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        done BOOLEAN NOT NULL,
        packer_id INTEGER,
        trip_id INTEGER NOT NULL, PRIMARY KEY (id), CHECK (done IN (0, 1)), FOREIGN KEY(packer_id) REFERENCES account (id), FOREIGN KEY(trip_id) REFERENCES trip (id)
)
```
