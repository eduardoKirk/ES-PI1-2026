CREATE DATABASE pi;
USE pi;

CREATE TABLE eleitores(
id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
nome VARCHAR(100) NOT NULL,
cpf VARCHAR(11) UNIQUE NOT NULL,
titulo_eleitor VARCHAR(12) UNIQUE NOT NULL,
mesario BOOLEAN DEFAULT false,
chave_acesso VARCHAR(255) NOT NULL,
status_voto BOOLEAN DEFAULT false
);

CREATE TABLE candidatos(
id_candidato INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(100) NOT NULL,
numero INT NOT NULL,
partido VARCHAR(50) NOT NULL
);

CREATE TABLE voto(
id_voto INT PRIMARY KEY AUTO_INCREMENT,
id_eleitor INT,
data_hora DATETIME,

FOREIGN KEY (id_eleitor) REFERENCES eleitores(id)
);

ALTER TABLE eleitores
MODIFY COLUMN cpf VARCHAR(255) UNIQUE NOT NULL;

INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso)
VALUES ("Eleitor Teste", "130201", "10320320", "1249124");
SELECT * FROM eleitores;

SELECT * FROM voto;

ALTER TABLE eleitores
DROP COLUMN status_votacao;

ALTER TABLE candidatos
ADD COLUMN numero_votos INT;

ALTER TABLE voto
MODIFY COLUMN protocolo_votacao VARCHAR(100) NOT NULL;

ALTER TABLE voto
ADD COLUMN status_voto boolean default false;

ALTER TABLE votos
DROP COLUMN id_eleitor;

ALTER TABLE votos
DROP FOREIGN KEY votos_ibfk_1;

ALTER TABLE votos
ADD COLUMN id_candidato INT;

ALTER TABLE votos
ADD FOREIGN KEY votos(id_candidato) REFERENCES candidatos(id_candidato);
