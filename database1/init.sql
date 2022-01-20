CREATE DATABASE pubsub;
use pubsub;

CREATE TABLE IF NOT EXISTS table_publishers (
  pub_identifier INT NOT NULL,
  topic_identifier INT NOT NULL
);


CREATE TABLE IF NOT EXISTS table_events (
  pub_identifier INT NOT NULL,
  topic_identifier INT NOT NULL,
  message_identifier INT NOT NULL AUTO_INCREMENT, 
  actual_message VARCHAR(250),
  PRIMARY KEY (message_identifier)
);

CREATE TABLE IF NOT EXISTS table_subscriptions (
  topic_identifier INT,
  -- topic VARCHAR(100) NOT NULL,
  sub_identifier INT NOT NULL
);