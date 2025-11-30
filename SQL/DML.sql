-- Insertion dans Personne
INSERT INTO Personne (nom, prenom, sexe, date_naissance, mail, tel, login, mot_de_passe) VALUES
('Dupont', 'Alice', 'femme', '1995-02-15', 'alice.dupont@mail.com', '0612345671', 'user01', '$2y$10$5ozcep67XkxrvBztGBOtZepHS6DMcoDK/9g0DxFz3hKQfFF810c9u'),
('Martin', 'Bob', 'homme', '1990-06-20', 'bob.martin@mail.com', '0612345672', 'bob_', '$2y$10$5ozcep67XkxrvBztGBOtZepHS6DMcoDK/9g0DxFz3hKQfFF810c9u'),
('Durand', 'Caroline', 'femme', '1988-11-05', 'caroline.durand@mail.com', '0612345673', 'Caro', '$2y$10$ZaWNAk9dr3SHxBGPWd2bee7TwgiQhgAImMa7/PXwH6OibjMCOFfB6'),
('Lefevre', 'David', 'homme', '1992-03-30', 'david.lefevre@mail.com', '0612345674', 'DAVID', '$2y$10$NayLrL1dtZ0aG4uYPIdVyuCmGDfreyOb3TLZ/OKK1u5kjzb6jlrs.'),
('Moreau', 'Emma', 'femme', '1997-08-12', 'emma.moreau@mail.com', '0612345675', 'Ma', '$2y$10$3ZXeNSYAEPySHB9SmSfEt.BXGgWCJlWcXR7mihzoWQrTX4ypYEb02'),
('Petit', 'Franck', 'homme', '1985-05-10', 'franck.petit@mail.com', '0612345676', 'Franc', '$2y$10$1t7ME9ZTIEqPaF.He7m8FejbLd0zH/OvSROgtJCeb4LLGSRutJyIy'),
('Rousseau', 'Gina', 'femme', '1991-07-22', 'gina.rousseau@mail.com', '0612345677', 'Gina', '$2y$10$56WrwMzFld5nWzCT3Les6.VUC84.6UnrHCDTQDfBh8pNf0lfePPTK'),
('Blanc', 'Hugo', 'homme', '1993-12-11', 'hugo.blanc@mail.com', '0612345678', 'white', '$2y$10$65w5XV2PslXmSj7z7nR3CeJvqTpSXAPTyff7uXuUw3cqVqj23pr9G'),
('Morel', 'Isabelle', 'femme', '1989-09-01', 'isabelle.morel@mail.com', '0612345679', 'ISA', '$2y$10$C5bgpDXUJPLzt5PB2SQgfe2YugPR352qLZzlMcDCn2.guzGicnfRi'),
('Girard', 'Jacques', 'homme', '1994-04-18', 'jacques.girard@mail.com', '0612345680', 'PasDebol', '$2y$10$INBblDp34vs9EkXC3AOyT.WTXloiCorJYMy.ohmi6nYV/SHx07/Ga');

-- Insertion dans Client
INSERT INTO Client (id_client, pseudo, solde_jetons, date_inscription) VALUES
(1, 'Alice95', 100, '2023-01-10'),
(2, 'Bob90', 50, '2023-02-15'),
(3, 'Caroline88', 200, '2023-03-20'),
(4, 'David92', 75, '2023-04-25'),
(5, 'Emma97', 150, '2023-05-30');

-- Insertion dans Admin
INSERT INTO Admin (id_admin, date_anciennete_employe, poste_employe, status_employe) VALUES
(6, '2020-01-01', 'gerant', 'travail'),
(7, '2021-06-15', 'nettoyage', 'en_pause'),
(8, '2019-09-10', 'personnel', 'travail'),
(9, '2022-03-20', 'gerant', 'repos'),
(10, '2020-11-05', 'personnel', 'travail');

-- Insertion dans Fournisseur
INSERT INTO Fournisseur (nom_four, mail_four, tel_four, adresse_four) VALUES
('Nintendo', 'contact@nintendo.com', '0611122233', '12 rue du Jeu, Tokyo'),
('Capcom', 'support@capcom.com', '0622233344', '45 avenue du Fun, Osaka'),
('Sega', 'info@sega.com', '0633344455', '78 boulevard Play, Tokyo'),
('Konami', 'sales@konami.com', '0644455566', '9 rue Arcade, Tokyo'),
('Atari', 'contact@atari.com', '0655566677', '22 rue Jeton, Paris');

-- Insertion dans Jeux
INSERT INTO Jeux (nom, etat_jeu) VALUES
('Pacman', 'Disponible'),
('Super Mario', 'Disponible'),
('Tetris', 'En Maintenance'),
('Zelda', 'Disponible'),
('Donkey Kong', 'HS');

-- Insertion dans Jeux_Solo
INSERT INTO Jeux_Solo (id_jeux_solo, difficulte) VALUES
(1, 'Facile'),   
(2, 'Normal'),   
(3, 'Difficile');

-- Insertion dans Jeux_Multi
INSERT INTO Jeux_Multi (id_jeux_multi, type_equipe, nb_joueur_min, nb_joueur_max) VALUES
(4, 'vs', 2, 4), 
(5, 'Coop', 4, 4);

-- Insertion dans Carte
INSERT INTO Carte (status_carte, date_carte, version_carte, id_client) VALUES
('Liee', '2023-01-11', 1, 1),
('Liee', '2023-02-16', 1, 2),
('Perdu', '2023-03-21', 2, 4),
('Liee', '2023-04-26', 2, 4),
('Liee', '2023-05-31', 1, 5);

-- Insertion dans Recharge
INSERT INTO Recharge (montant_jeton, mode_paiement, date_recharge, id_carte) VALUES
(50, 'CB', '2023-01-15', 1),
(100, 'espece', '2023-02-20', 2),
(75, 'CB', '2023-03-25', 3),
(150, 'CB', '2023-04-30', 4),
(200, 'espece', '2023-06-05', 5);

-- Insertion dans Borne
INSERT INTO Borne (etat_borne, prix_jeton, date_achat, id_four) VALUES
('Disponible', 5, '2022-01-01', 1),
('En Maintenance', 10, '2022-06-15', 2),
('Disponible', 7, '2022-09-10', 3),
('HS', 5, '2023-03-20', 4),
('Disponible', 8, '2023-11-05', 5);

-- Insertion dans Jeux_Borne
INSERT INTO Jeux_Borne (id_jeux, id_borne) VALUES
-- Insertion dans Borne 1
(1, 1),
(2, 1),
-- Insertion dans Borne 2
(5, 2),
-- Insertion dans Borne 3
(1, 3),
(3, 3),
(4, 3),
-- Insertion dans Borne 5
(1, 5),
(2, 5),
(3, 5),
(4, 5),
(5, 5); 

-- Insertion dans Partie
INSERT INTO Partie (score, date_partie, recompense, status_partie, id_client, id_jeux, id_borne) VALUES
(100, '2023-07-01', 0, 'Termine', 5, 1, 1),
(85000, '2023-07-02', 2,'Recompense donnee', 5, 2, 5),
(50, '2023-07-03', 1,'Recompense donnee', 1, 1, 3),
(120, '2023-07-04', 5,'Recompense donnee', 3, 4, 5),
(NULL, '2025-11-09', 0,'En cours', 4, 2, 5);
