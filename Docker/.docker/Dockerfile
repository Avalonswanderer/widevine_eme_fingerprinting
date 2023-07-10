FROM php:7.3-apache

RUN mkdir /app

RUN mkdir /etc/apache2/sites-available/ssl

COPY .docker/apache/localhost* /etc/apache2/sites-available/ssl/
COPY .docker/apache/vhost.conf /etc/apache2/sites-available/000-default.conf

WORKDIR /app

RUN chown -R www-data:www-data /app && a2enmod rewrite ssl && a2enmod dump_io
