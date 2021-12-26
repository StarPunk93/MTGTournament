
CREATE TABLE `Players`
(
 `id`   integer NOT NULL AUTO_INCREMENT,
 `name` varchar(100) NOT NULL ,

PRIMARY KEY (`id`)
);


CREATE TABLE `Match`
(
 `id`      integer NOT NULL AUTO_INCREMENT,
 `player1` integer NOT NULL ,
 `player2` integer NOT NULL ,
  `winner`  integer NULL,

PRIMARY KEY (`id`),
KEY `FK_46` (`player1`),
CONSTRAINT `FK_44` FOREIGN KEY `FK_46` (`player1`) REFERENCES `Players` (`id`),
KEY `FK_49` (`player2`),
CONSTRAINT `FK_47` FOREIGN KEY `FK_49` (`player2`) REFERENCES `Players` (`id`)
);

CREATE TABLE `Decks`
(
 `id`        integer NOT NULL AUTO_INCREMENT,
 `player_id` integer NOT NULL ,

PRIMARY KEY (`id`),
KEY `FK_15` (`player_id`),
CONSTRAINT `FK_13` FOREIGN KEY `FK_15` (`player_id`) REFERENCES `Players` (`id`)
);

CREATE TABLE `cards`
(
 `cardid`        integer AUTO_INCREMENT,
 `id`            varchar(36) DEFAULT NULL,
 `name`          varchar(51) DEFAULT NULL ,
 `manaCost`      varchar(12) DEFAULT NULL  ,
 `cmc`           decimal(2,1) DEFAULT NULL  ,
 `colors`        varchar(18) DEFAULT NULL  ,
 `colorIdentity` varchar(10) DEFAULT NULL  ,
 `type`          varchar(36) DEFAULT NULL  ,
 `types`         varchar(24) DEFAULT NULL  ,
 `rarity`        varchar(8) DEFAULT NULL  ,
 `set`           varchar(3) DEFAULT NULL ,
 `setName`       varchar(22) DEFAULT NULL  ,
 `text`          text DEFAULT NULL  ,
 `flavor`        varchar(179) DEFAULT NULL  ,
 `artist`        varchar(23) DEFAULT NULL  ,
 `number`        smallint(6) DEFAULT NULL  ,
 `layout`        varchar(9) DEFAULT NULL  ,
 `multiverseid`  mediumint(9) DEFAULT NULL  ,
 `imageUrl`      varchar(77) DEFAULT NULL  ,
 `foreignNames`  text DEFAULT NULL  ,
 `printings`     text DEFAULT NULL  ,
 `originalText`  text DEFAULT NULL  ,
 `originalType`  varchar(36) DEFAULT NULL  ,
 `legalities`    text DEFAULT NULL  ,
 `subtypes`      varchar(32) DEFAULT NULL  ,
 `power`         varchar(3) DEFAULT NULL  ,
 `toughness`     varchar(3) DEFAULT NULL  ,
 `variations`    varchar(120) DEFAULT NULL  ,
 `supertypes`    varchar(13) DEFAULT NULL  ,
 `rulings`       text DEFAULT NULL  ,
 `loyalty`       varchar(3) DEFAULT NULL  ,
 `watermark`     varchar(12) DEFAULT NULL  ,

PRIMARY KEY (`cardid`)
);

CREATE TABLE `Decks_Cards`
(
 `id`      integer NOT NULL AUTO_INCREMENT,
 `deck_id` integer NOT NULL ,
 `card_id` integer NOT NULL ,

PRIMARY KEY (`id`),
KEY `FK_21` (`deck_id`),
CONSTRAINT `FK_19` FOREIGN KEY `FK_21` (`deck_id`) REFERENCES `Decks` (`id`),
KEY `FK_97` (`card_id`),
CONSTRAINT `FK_95` FOREIGN KEY `FK_97` (`card_id`) REFERENCES `cards` (`cardid`)

);
