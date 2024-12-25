CREATE DATABASE social_media_data;
USE social_media_data;

CREATE TABLE posts (
    collected_time DATETIME DEFAULT NULL,
    comments INT DEFAULT NULL,
    likes INT DEFAULT NULL,
    link_img TEXT DEFAULT NULL,
    link_post TEXT DEFAULT NULL,
    post_content TEXT DEFAULT NULL,
    post_id INT NOT NULL AUTO_INCREMENT,
    shares INT DEFAULT NULL,
    url_page TEXT DEFAULT NULL,
    PRIMARY KEY (post_id)
);
CREATE TABLE posts (
    collected_time DATETIME DEFAULT NULL,
    comments INT DEFAULT NULL,
    likes INT DEFAULT NULL,
    link_img TEXT DEFAULT NULL,
    link_post TEXT DEFAULT NULL,
    post_content TEXT DEFAULT NULL,
    post_id INT NOT NULL AUTO_INCREMENT,
    shares INT DEFAULT NULL,
    url_page TEXT DEFAULT NULL,
    PRIMARY KEY (post_id)
);
CREATE TABLE profiles (
    cover_image TEXT DEFAULT NULL,
    detail TEXT DEFAULT NULL,
    logo_image TEXT DEFAULT NULL,
    num_follower INT DEFAULT 0,
    num_following INT DEFAULT 0,
    num_like INT DEFAULT 0,
    post_photos TEXT DEFAULT NULL,
    profile_id INT NOT NULL AUTO_INCREMENT,
    url TEXT DEFAULT NULL,
    PRIMARY KEY (profile_id)
)




















