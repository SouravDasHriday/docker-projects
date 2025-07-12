# Start from the official PHP image with Apache web server
FROM php:8.1-apache

# Install the mysqli extension for PHP to talk to MySQL
RUN docker-php-ext-install mysqli

# Enable the rewrite module for Apache (good practice)
RUN a2enmod rewrite
