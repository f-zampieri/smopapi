# smop. API
Welcome to the API! Below is some info on what I am using:

## Lang/Lib:
* html
* css
* js
* python (see note)
  * digitalocean -- servers
  * paramiko -- ssh
  * pysendfile & socket -- ftp
  * other: os, sys, time, subprocess, JSON
  * pip -- installing libraries for use with python
* node
* express (no pug, but see below on how to make a page)
* bootstrap
* jquery
* mongodb
* mongoose
* jsonwebtoken
* bash

## Some Helpful Resources 
* http://justbuildsomething.com/node-js-best-practices/#3
* https://zellwk.com/blog/crud-express-mongodb/
* https://scotch.io/tutorials/authenticate-a-node-js-api-with-json-web-tokens

## General Etiquette (applicable on *all* files)
* Use Beautify.io to get the right styling. I use Brackets which has a plugin for it

## html/Pug Etiquette (aka how to make a page)
* html and Pug files are located in the views folder
* html files are included in Jade files
* Pug files are processed into client facing files (eg - if I wanted a page called user.html, it would be called user.pug in the views folder and have 2+ lines of code, all of which are includes to html files *see index.pug for example*
* **header.html *must* be included in all Pug files**
* **only html files may be included in Pug files**
* Each page's html file must close the header before beginning a body
* headers should not include anything that can be seen by the user

## JS Etiquette
* **no javascripts in html documents,** *they belong in .js documents in the /public/javascripts folder and are to be linked via* \<script src="/public/javascripts/mysource.js">\</script>

## API Etiquette 
* **never call localhost:3001/api/... from outside of api**, make a function in the API to do so

## Notes on Python:
* **To use PythonBackend** - read file block comment for install instructions and version info

## Notes on Bash:
* **All Bash (.sh) files are called from [js]setup.sh** - this file is called by Python
* Don't use any extra whitespace in [js]setup.sh file, it is read line by line by python and executed as commands
