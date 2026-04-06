CREATE DATABASE pi;
USE pi;
CREATE TABLE eleitores(
id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
nome VARCHAR(100) NOT NULL,
cpf INT UNIQUE NOT NULL,
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
id_candidatos INT,
data_hora DATETIME,

FOREIGN KEY (id_candidatos) REFERENCES candidatos(id_candidato),
FOREIGN KEY (id_eleitor) REFERENCES eleitores(id)
);

INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso)
VALUES ("Eleitor Teste", "130201", "10320320", "1249124");


