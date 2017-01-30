#smop. API
Welcome to the API! Below is some info on what I plan on using:

##Lang/lib:
* html
* css
* js
* node.js
* express (no pug, but see below on how to make a page)
* bootstrap
* jquery
* angular.js --> maybe

##Some Helpful Resources 
* http://justbuildsomething.com/node-js-best-practices/#3
* https://zellwk.com/blog/crud-express-mongodb/

##html/Pug Etiquette (aka how to make a page)
* html and Pug files are located in the views folder
* html files are included in Jade files
* Pug files are processed into client facing files (eg - if I wanted a page called user.html, it would be called user.pug in the views folder and have 2+ lines of code, all of which are includes to html files *see index.pug for example*
* **header.html *must* be included in all Pug files**
* **only html files may be included in Pug files**
* Each page's html file must close the header before beginning a body
* headers should not include anything that can be seen by the user

##JS Etiquette
* Since express is awesome, we probably don't have to write much node stuff for now
* **no javascripts in html documents,** *they belong in .js documents in the /public/javascripts folder and are to be linked via* \<script src="/public/javascripts/mysource.js">\</script>
