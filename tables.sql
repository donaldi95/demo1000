CREATE TABLE user (
    id INT NOT NULL auto_increment,
    username varchar(120) NOT NULL,
    password varchar(129) not null,
    email varchar(120) not null,
    PRIMARY KEY(id)
)   ENGINE=INNODB;

create table role(
	id int not null primary key auto_increment,
    role_type varchar(120) not null
) ENGINE=INNODB;

CREATE TABLE user_role (
	id int not null auto_increment,
    role_id INT NOT NULL,
    user_id int not null,
    PRIMARY KEY (id)
)   ENGINE=INNODB;

ALTER TABLE `user_role`
ADD CONSTRAINT `user_properties_foreign`
FOREIGN KEY (`role_id`)
REFERENCES `role` (`ID`)
ON DELETE NO ACTION
ON UPDATE NO ACTION;


ALTER TABLE `user_role`
ADD CONSTRAINT `user_role_properties_foreign`
FOREIGN KEY (`user_id`)
REFERENCES `user` (`ID`)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

CREATE TABLE campaign (
    id INT NOT NULL AUTO_INCREMENT primary key,
    user_id INT NOT NULL,
    username varchar(120) NOT NULL,
    start_date date NOT NULL,
    end_date date not null,
    status varchar(10) not null
)   ENGINE=INNODB;

ALTER TABLE `campaign`
ADD CONSTRAINT `campaign_properties_foreign`
FOREIGN KEY (`user_id`)
REFERENCES `user` (`ID`)
ON DELETE NO ACTION
ON UPDATE NO ACTION;


CREATE TABLE peaks (
    id INT NOT NULL AUTO_INCREMENT primary key,
    campaign_id INT NOT NULL,
    name varchar(120) NOT NULL,
    lat decimal(11,9) not null,
    lon decimal(10,9) not null,
    alt decimal(11,9) not null,
	local_name varchar(120) NOT NULL,
	provenance_origin varchar(120) NOT NULL,
    annodated varchar(10) not null
)   ENGINE=INNODB;

ALTER TABLE `peaks`
ADD CONSTRAINT `peaks_properties_foreign`
FOREIGN KEY (`campaign_id`)
REFERENCES `campaign` (`ID`)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

CREATE TABLE annotation (
    id INT NOT NULL AUTO_INCREMENT primary key,
    peak_id INT NOT NULL,
    user_id int not null,
    peak_validity varchar(120) not null,
	name varchar(120) NOT NULL,
	localized_names varchar(120) NOT NULL,
	creation_date date NOT NULL,
    status boolean
)   ENGINE=INNODB;

ALTER TABLE `annotation`
ADD CONSTRAINT `annotation_properties_foreign`
FOREIGN KEY (`peak_id`)
REFERENCES `peaks` (`ID`)
ON DELETE NO ACTION
ON UPDATE NO ACTION;


ALTER TABLE `annotation`
ADD CONSTRAINT `annotation_user_properties_foreign`
FOREIGN KEY (`user_id`)
REFERENCES `user` (`ID`)
ON DELETE NO ACTION
ON UPDATE NO ACTION;