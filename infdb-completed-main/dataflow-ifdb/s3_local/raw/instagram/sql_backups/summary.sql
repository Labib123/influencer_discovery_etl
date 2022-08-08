CREATE TABLE ig_summary(
   id                      VARCHAR(9) NOT NULL PRIMARY KEY
  ,followers               INTEGER  NOT NULL
  ,engagement              NUMERIC(19,17) NOT NULL
  ,num_recent_posts        INTEGER  NOT NULL
  ,post_frequency          NUMERIC(18,16) NOT NULL
  ,bio                     VARCHAR(12) NOT NULL
  ,profile_pic_url         VARCHAR(290) NOT NULL
  ,latest_posts        VARCHAR(304) NOT NULL
);
INSERT INTO ig_summary(id,followers,engagement,num_recent_posts,post_frequency,bio,profile_pic_url,latest_posts0url,latest_posts0likes) VALUES ('instagram',469095061,0.24985299875563538,39,1.2820512820512822,'#YoursToMake','https://instagram.fkul15-1.fna.fbcdn.net/v/t51.2885-19/203019087_3969530746500786_7930596639916235962_n.jpg?_nc_ht=instagram.fkul15-1.fna.fbcdn.net&_nc_cat=1&_nc_ohc=ZuLyhI_Nid4AX_54B1H&edm=AEF8tYYBAAAA&ccb=7-4&oh=00_AT_qgMH2OFS0v6f1z1FgruaN3r3_gur6pkmpaWaWgfC59g&oe=6203A582&_nc_sid=a9513d','https://instagram.fkul15-1.fna.fbcdn.net/v/t51.2885-15/e35/p1080x1080/273173383_119738723934091_8534072272838296411_n.jpg?_nc_ht=instagram.fkul15-1.fna.fbcdn.net&_nc_cat=1&_nc_ohc=HwB3gGzVCEIAX_uRy5K&edm=AAuNW_gBAAAA&ccb=7-4&oh=00_AT_ua6jCX-H5RskYxPxo_pM9FEHUWBjsRnWLemxHkDzCbw&oe=61FF2EE6&_nc_sid=498da5','170765',8415);
