# Shopcarts

[![Build Status](https://travis-ci.org/nyu-devops-echo/shopcarts.svg?branch=master)](https://travis-ci.org/nyu-devops-echo/shopcarts)
[![Codecov](https://img.shields.io/codecov/c/github/nyu-devops-echo/shopcarts.svg)]()

This is a RESTful shopcarts service that allows users to create, delete, and modify shopcarts.

## Running


1. `vagrant up`

2. `vagrant ssh`

3. `cd /vagrant`

4. `python3 run.py`


## Testing

1. `vagrant up`

2. `vagrant ssh`

3. `cd /vagrant`

4. `nosetests`

## RESTful API
#### Overview
  * user_id and product_id are always integers

#### GET /
  * Root URL

#### GET /shopcarts
  * Retrieves all shopcarts

#### GET /shopcarts/user_id
  * Retrieves the shopcart for user_id

#### GET /shopcarts?pid=product_id
  * Queries all shopcarts for a specified product_id

#### DELETE /shopcarts/user_id
  * Deletes the shopcart for user_id

#### POST /shopcarts
  * Creates a new shopcart for user_id and optional dictionary of {product_id : product_quantity} pairs to place in the shopcart

#### POST /shopcarts/user_id/products
  * Adds a product to the shopcart for user_id, where the product added is a dictionary of the {product_id : product_quantity}

#### PUT /shopcarts/user_id/products/product_id
  * Updates product_id's quantity in user_id's shopcart, where the updated quantity is in a dictionary {product_id: new_quantity}

#### DELETE /shopcarts/user_id/products/product_id
  * Deletes product_id from user_id's shopcart

#### DELETE /shopcarts/prune
  * Deletes all empty shopcarts

## Build Shopcarts UI

``` bash
cd /vagrant

# install dependencies
npm install

# watch changes and rebuild
npm run watch

# build for production with minification
npm run build
```

Built using [Vue.js](https://vuejs.org)