CREATE TABLE ig_meta(
   id                     VARCHAR(20) NOT NULL PRIMARY KEY
  ,followers              INTEGER  NOT NULL
  ,following              INTEGER  NOT NULL
  ,bio                    VARCHAR(150)
  ,profile_pic_url        VARCHAR(292) NOT NULL
  ,business_category_name VARCHAR(43) NOT NULL
  ,media_count            INTEGER  NOT NULL
  ,external_url           VARCHAR(106)
  ,is_verified            VARCHAR(4) NOT NULL
  ,full_name              VARCHAR(26) NOT NULL
  ,is_business_account    VARCHAR(5) NOT NULL
);
INSERT INTO mytable(id,followers,following,bio,profile_pic_url,business_category_name,media_count,external_url,is_verified,full_name,is_business_account) VALUES ('natgeo',216439614,137,'Experience the world through the eyes of National Geographic photographers.','https://instagram.fkul15-1.fna.fbcdn.net/v/t51.2885-19/277603428_552076426529300_897951030206377110_n.jpg?_nc_ht=instagram.fkul15-1.fna.fbcdn.net&_nc_cat=1&_nc_ohc=QsTvm7rS0y0AX8OBSvc&edm=AEF8tYYBAAAA&ccb=7-4&oh=00_AT9nkG0cffnE6yIeWYpeSPNHel0tKWhsY5iuromFiMfOfQ&oe=62578132&_nc_sid=a9513d','Publishers',26576,'https://on.natgeo.com/instagram','true','National Geographic','true');
INSERT INTO mytable(id,followers,following,bio,profile_pic_url,business_category_name,media_count,external_url,is_verified,full_name,is_business_account) VALUES ('taylorswift',206143462,0,'Happy, free, confused and lonely at the same time.