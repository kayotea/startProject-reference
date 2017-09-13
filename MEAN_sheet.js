"Start Project"

//in terminal
mkdir [[project_name]]
cd [[project_name]]

//set up dependencies: still in terminal
npm init -y //-y sets "yes" answer to initialization q's
npm install express --save
npm install body-parser --save
npm install mongoose --save

//now take a look at package.json file to make sure everything is there

//~~~~~~~~~~

"Add Modularity"
//in terminal, on the same level as package.json
touch server.js
mkdir server

mkdir server/config
touch server/config/mongoose.js
touch server/config/routes.js

mkdir server/controller
touch server/controller/[[items.js]]
//replace [[items.js]] with whatever your object is called
//it's a good idea to have a separate [[items.js]] for each type of object
//for readability/modularity

mkdir server/models
touch server/models[[item.js]]
//[[item.js]] should correspond to the [[items.js]] in the controller folder

//~~~~~~~~~~

"Add Angular"
//in terminal, on the same level as package.json"

//angular WITHOUT routing built in:
ng new public //make sure this command doesn't create a nested Git repo

//angular WITH routing built in:
ng new public --routing //make sur enot nested git repo

//if you created an nangular project without routing, and decide later that you would like to have routing:
ng g module app-routing //g is short for 'generate'

//back go business: contiue setting up Angular
cd public
ng build -w //this is necessary to run updated server later

//if you'd like to add cookies, this is a good open-source option:
//documentation here: https://www.npmjs.com/package/angular2-cookie
npm install angular2-cookie --save

//~~~~~~~~~~

"BOILERPLATE SETUP:"
"server.js"
/*
 * SETUP
 */
const express = require('express'),
mongoose = require('mongoose'),
bodyParser = require('body-parser'),
path = require('path'),
app = express();

app.use(bodyParser.json());//use bodyParser with json
//note: there are different ways to use bodyParser... pick what works for you
app.use(express.static(path.join(__dirname, './public/dist')));//connect angular

/*
* ROUTES
*/
require('./server/config/mongoose.js');
var routes_setter = require('./server/config/routes.js');
routes_setter(app);

/*
* SERVER PORT 
*/
app.listen(8000, function(){
console.log('listening on port 8000');
});

"mongoose.js"
/*
 * VARIABLES
 */

var mongoose = require('mongoose');//get mongoose
var fs = require('fs');//for loading model files
var path = require('path');//use to get models path

//1 - connect to database
mongoose.connect('mongodb://localhost/[[DATABASE NAME]]');

//2 - point to where models live
var models_path = path.join(__dirname, '../models');

//3 - load models in models path
fs.readdirSync(models_path).forEach(function(file){
    if (file.indexOf('.js') >= 0){
        //run model file w/ schema
        require(models_path + '/' + file);
    }
});

"routes.js" //add CRUD
/*
 * VARIABLES
 */
var quotes = require('../controller/[[ITEMS]].js'),
path = require('path');

/*
* ROUTES
*/
module.exports = function(app){

app.post('/newitem', (req, res) => {
    items.createItem(req, res);
});
app.get('/items', (req, res) => {
    items.index(req, res);
});
app.post('/delete/item', (req, res) => {
    console.log('reached routes.js/app.delete()');
    items.deleteItem(req, res);
})
//and overflow:
app.all("*", (req,res) => {
    res.sendfile(path.resolve("./public/dist/index.html"));
});
}

"items.js" //add CRUD
/*
 * VARIABLES
 */
var mongoose = require('mongoose');
var Item = mongoose.model('Item');
mongoose.Promise = global.Promise;

var path = require('path');

/*
 * LOGIC
 */

module.exports = {

    index: function(req, res){
        Item.find({})
        .then(data => {
            console.log('success in items.js/findNotes()');
            res.json(data);
        })
        .catch(err => {
            console.log('error in items.js/findNotes()');
            res.json(err);
        })
    },

    createItem: function(req, res){
        var item = new Item(req.body);
        item.save(item)
        .then(data => {
             console.log('success in items.js/createNote()');
             res.json(data);
        })
        .catch(err => {
            console.log('error in items.js/createNote()');
            res.json(err);
        })
    },

    deleteItem: (req, res) => {
        console.log("deleteitem(): item is:",req.body);
        Item.deleteOne(req.body.id)
        .then(data => {
            console.log('success in items.js/deleteItem()');
            res.json(data);
        })
        .catch(err => {
            console.log('error in items.js/deleteItem()');
            res.json(err);
        })
    }
}

"item.js"
/*
 * ITEM MODEL 
 */
var mongoose = require('mongoose');
mongoose.Promise = global.Promise;
//create schema
var ItemSchema = new mongoose.Schema({
    created: Date,
    note: String
}, {timestamp: true});

//register schema as model
var Item = mongoose.model('Item', ItemSchema);

//~~~~~~~~~~

"Add Service to Angular App"
//in terminal:
cd public/src/app
ng g service http "[[name_of_service]]" //generates http.service.ts file

"app/http.service.ts"
import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs'

@Injectable()
export class HttpService {

  constructor(private _http: Http) { }

  retrieveItems() {
    return this._http.get('/notes')
    .map( data => data.json() )
    .toPromise();
  }
  makeItem(item) {
    return this._http.post('/newitem', item)
    .map((data) => data.json())
    .toPromise();
  }
}

"app/app.module.ts"
//make sure that you include the service you created here
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { HttpService } from './http.service';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [HttpService],
  bootstrap: [AppComponent]
})
export class AppModule { }
//~~~~~~~~~~

"Generate Component for Angular App"
ng g c [[component_name]]//'c' is short for 'component'

"Generate Class for Angular App"
ng g class [[class_name]]//do NOT shorten 'class' to 'c'