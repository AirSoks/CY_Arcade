-- Table : Personne
CREATE TABLE Personne (
	id_perso SERIAL PRIMARY KEY,
	nom VARCHAR(25) NOT NULL,
	prenom VARCHAR(25) NOT NULL,
	sexe VARCHAR(10) NOT NULL CHECK (sexe IN ('homme', 'femme')),
	date_naissance DATE NOT NULL,
	mail VARCHAR(40) NOT NULL UNIQUE,
	tel CHAR(10) UNIQUE,
	login VARCHAR(25) NOT NULL UNIQUE,
	mot_de_passe VARCHAR(255) NOT NULL
);

-- Table : Client
CREATE TABLE Client(
	id_client INT PRIMARY KEY REFERENCES Personne(id_perso)
        ON DELETE CASCADE ON UPDATE CASCADE,
	pseudo VARCHAR(25) NOT NULL UNIQUE,
	solde_jetons INT NOT NULL DEFAULT 0 CHECK (solde_jetons >= 0),
	date_inscription DATE NOT NULL DEFAULT (CURRENT_DATE)
);

-- Table : Admin
CREATE TABLE Admin(
	id_admin INT PRIMARY KEY REFERENCES Personne(id_perso)
        ON DELETE CASCADE ON UPDATE CASCADE,
	date_anciennete_employe DATE NOT NULL DEFAULT (CURRENT_DATE),
	poste_employe VARCHAR(10) NOT NULL CHECK (poste_employe IN ('gerant', 'nettoyage', 'personnel')),
	status_employe VARCHAR(10) NOT NULL DEFAULT 'travail' CHECK (status_employe IN ('travail', 'en_pause', 'repos'))
);

-- Table : Carte
CREATE TABLE Carte(
	id_carte SERIAL PRIMARY KEY,
	status_carte VARCHAR(10) NOT NULL DEFAULT 'Liee' CHECK (status_carte IN ('Perdu', 'Liee')),
	date_carte DATE NOT NULL DEFAULT (CURRENT_DATE),
	version_carte INT NOT NULL CHECK (version_carte > 0),
	id_client INT NOT NULL REFERENCES Client(id_client)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table : Recharge
CREATE TABLE Recharge(
	id_recharge SERIAL PRIMARY KEY,
	montant_jeton INT NOT NULL CHECK (montant_jeton >0),
	mode_paiement VARCHAR(10) NOT NULL CHECK (mode_paiement IN ('CB', 'espece')),
	date_recharge DATE NOT NULL,
	id_carte INT NOT NULL REFERENCES Carte(id_carte)
		ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table : Fournisseur
CREATE TABLE Fournisseur(
	id_four SERIAL PRIMARY KEY,
	nom_four VARCHAR(20) NOT NULL,
	mail_four VARCHAR(40) NOT NULL UNIQUE,
	tel_four CHAR(10) NOT NULL UNIQUE,
	adresse_four VARCHAR(30) NOT NULL
);

-- Table : Jeux
CREATE TABLE Jeux(
	id_jeux SERIAL PRIMARY KEY,
	nom VARCHAR(50) NOT NULL UNIQUE,
	etat_jeu VARCHAR(15) NOT NULL DEFAULT 'Disponible' CHECK (etat_jeu IN ('Disponible', 'En Maintenance', 'HS'))
);        

-- Table : Jeux_Solo
CREATE TABLE Jeux_Solo(
	id_jeux_solo INT PRIMARY KEY REFERENCES Jeux(id_jeux)
        ON DELETE CASCADE ON UPDATE CASCADE,
	difficulte VARCHAR(10) NOT NULL CHECK (difficulte IN ('Facile', 'Normal', 'Difficile'))
);

-- Table : Jeux_Multi
CREATE TABLE Jeux_Multi(
	id_jeux_multi INT PRIMARY KEY REFERENCES Jeux(id_jeux)
        ON DELETE CASCADE ON UPDATE CASCADE,
	type_equipe VARCHAR(4) NOT NULL CHECK (type_equipe IN ('Coop', 'vs')),
	nb_joueur_min INT NOT NULL,
	nb_joueur_max INT NOT NULL,
	CHECK (nb_joueur_min >= 2 AND nb_joueur_max <= 4 AND nb_joueur_min <= nb_joueur_max)
);

-- Table : Borne
CREATE TABLE Borne(
	id_borne SERIAL PRIMARY KEY,
	etat_borne VARCHAR(15) NOT NULL DEFAULT 'Disponible' CHECK (etat_borne IN ('Disponible', 'En Maintenance', 'HS')),
	prix_jeton INT NOT NULL CHECK (prix_jeton > 0),
	date_achat DATE NOT NULL DEFAULT (CURRENT_DATE),
	id_four INT NOT NULL REFERENCES Fournisseur(id_four)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table : Jeux_Borne
CREATE TABLE Jeux_Borne (
    id_jeux INT NOT NULL REFERENCES Jeux(id_jeux)
        ON DELETE CASCADE ON UPDATE CASCADE,
    id_borne INT NOT NULL REFERENCES Borne(id_borne)
        ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_jeux, id_borne)
);	

-- Table : Partie
CREATE TABLE Partie (
	id_partie SERIAL PRIMARY KEY,
	score INT CHECK (score >= 0),
	date_partie DATE,
	recompense INT NOT NULL DEFAULT 0 CHECK (recompense IN (5, 2, 1, 0)),
	status_partie VARCHAR(20) NOT NULL DEFAULT 'En cours' CHECK (status_partie IN ('En cours', 'Termine', 'Recompense donnee')),
	id_client INT NOT NULL REFERENCES Client(id_client),
	id_jeux INT NOT NULL REFERENCES Jeux(id_jeux)
        ON DELETE CASCADE ON UPDATE CASCADE,
	id_borne INT NOT NULL REFERENCES Borne(id_borne)
        ON DELETE CASCADE ON UPDATE CASCADE
);