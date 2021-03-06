Baruwa (swahili for letter or mail) is a web 2.0 `MailScanner <http://www.mailscanner.info/>`_
front-end. 

It provides an easy to use interface for managing a MailScanner installation. It is used to
perform operations such as releasing quarantined messages, bayesian learning, whitelisting and 
blacklisting addresses, monitoring the health of the services etc. Baruwa is implemented 
using web 2.0 features (AJAX) where deemed fit, graphing is also implemented on the client
side using SVG, Silverlight or VML. Baruwa has full support for i18n, letting you support 
any language of your choosing.

It includes reporting functionality with an easy to use query builder, results can be 
displayed as message lists or graphed as colorful and pretty interactive graphs.

Custom MailScanner modules are provided to allow for logging of messages to the mysql
database with SQLite as backup, managing whitelists and blacklists and managing per
user spam check settings.

Baruwa is open source software, written in Python/Perl using the Django Framework and 
MySQL or PostgreSQL for storage, it is released under the GPLv2 and is available for
free download.