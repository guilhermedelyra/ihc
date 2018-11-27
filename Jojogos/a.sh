#!/bin/bash
set -x
rails _5.1.4_ new .

echo "gem 'solidus'" >> Gemfile
echo "gem 'solidus_auth_devise'" >> Gemfile
echo "gem 'deface'" >> Gemfile
echo "gem 'solidus_i18n'" >> Gemfile
echo "gem 'rails-i18n', '~> 5.1'" >> Gemfile
echo "gem 'kaminari-i18n', '~> 0.5.0'" >> Gemfile

sudo bundle install

sudo bundle exec rails db:create

sudo bundle exec rails g spree:install
sudo bundle exec rails g solidus:auth:install
sudo bundle exec rails g solidus_i18n:install
sudo bundle exec rails railties:install:migrations
sudo bundle exec rails db:migrate
mkdir -p app/controllers/spree
cp ~/solidus/frontend/app/controllers/spree/home_controller.rb app/controllers/spree