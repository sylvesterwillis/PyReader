PyReader
========

Saw a mention of Google's RSS reader shutting down, and figured that I would create a RSS reader as a project.

Tasks Completed
===============
1. Learn more about Python/Django and create prototype of the site.
    * Implemented user login, register, and logout.
    * Implemented addition and removal of rss feeds by user.
    * Implemented displaying of feeds by user.

Instructions for deployment on ec2
==================================
1. Go to /etc/apache2/sites-available and create file for PyReader, then setup VirtualHost using a Django with mod_wsgi tutorial.
    * If there is already a file for PyReader, then check to see if the servername matches the ec2 instance public DNS.
2. Restart Apache2 using "sudo service apache2 restart".
