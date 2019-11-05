> show dbs
admin  0.000GB
local  0.000GB

> use mydb
switched to db mydb

> db
mydb

> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB

> db.movie.insert({"name":"tutorial"})
WriteResult({ "nInserted" : 1 })

> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
mydb    0.000GB

> db.dropDatabase()
{ "dropped" : "mydb", "ok" : 1 }

> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB

# 2.2 MongoDB – Construção de queries
    > mongoimport --db cbd --collection rest --drop --file restaurants.json
    2019-10-17T09:53:14.632+0100	connected to: localhost
    2019-10-17T09:53:14.635+0100	dropping: cbd.rest
    2019-10-17T09:53:15.416+0100	imported 3772 documents

    > mongo
        > use cbd
        switched to db cbd

        > db.rest.count()
        3772

_________________________________________________________________________________________________________________________________________________________________________________

    #1
        > db.rest.find()
    
    #2
        > db.rest.find({},{restaurant_id:1 ,nome: 1,localidade: 1,gastronomia: 1}).pretty()
        // Este comando corresponde a "SELECT restaurant_id, nome ,localidade, gastronomia FROM rest" em SQL
        // Exemplo de output:
        //  {
        //  	"_id" : ObjectId("5da82bfaa4a583bfb1df354e"),
        //  	"localidade" : "Brooklyn",
        //  	"gastronomia" : "American",
        //  	"nome" : "The Movable Feast",
        //  	"restaurant_id" : "40361606"
        //  }
        //  (...)

    #3
        > db.rest.find({},{_id:0,restaurant_id:1,nome:1,localidade: 1,gastronomia: 1,'address.zipcode':1}).pretty()
        // _id: 0 --> Para ocultar o _id
        // address.zipcode --> para ir buscar o zipcode no array address

    #4
        > db.rest.find({localidade:"Bronx"},{_id:0, nome:1}).pretty()
        // Este comando corresponde a "SELECT nome,localidade FROM rest WHERE localidade = 'Bronx'" em SQL
        // Alguns outputs:
        //    { "nome" : "Morris Park Bake Shop" }
        //    { "nome" : "Wild Asia" }
        //    { "nome" : "Carvel Ice Cream" }
        //      (...)

    #5
        > db.rest.find({localidade:"Bronx"},{_id:0, nome:1}).pretty().limit(5)
        // limit(N) vai limitar o output a N resultados.

    #6
        > db.rest.find({ "grades" : { $elemMatch: { score: { $gt:85 } } } } ,{_id:0}).pretty()

    
    #7
        > db.rest.find({ "grades" : { $elemMatch: { score: { $gt:80, $lt:100 } } } } ,{_id:0}).pretty()

    #8
        > #db.rest.find({"address" : { $arrayElemAt : ["$coords",0] }, { _id:0}).pretty() ??????????????????????????

          #db.rest.find( { address: { $elemMatch: {  $arrayElemAt : [ "$coord" , 0 ] }: { $lt: -95 } } ).pretty()

          #db.rest.find( { "address.coord.0" { $elemMatch: { $lt: -95 }}}).pretty()

          db.rest.find( { "address.coord.0":  { $lt: -95.7 }}).pretty()

    #9
        > db.rest.find({ gastronomia: { $ne : "American" } }).pretty()
        // Receber todos os restaurantes cuja gastronomia não é American
        > db.rest.find( { $and : [ { gastronomia: { $ne : "American" }}, { "grades.score" :{ $gt:70 } }, { "address.coord.0":  { $lt: -65 }} ] }).pretty().limit(1)

    #10
        > db.rest.find({nome:{ $regex: "Wil*"}},{_id:0,nome:1,restaurant_id:1,gastronomia:1,localidade:1}).pretty()

    #11
        > db.rest.find({ $and : [ {localidade: "Bronx"}, {$or : [{gastronomia: "American"},{gastronomia: "Chinese" }]}]},{_id:0,nome:1,gastronomia:1,localidade:1}).pretty()

    #12
        > db.rest.find({$or : [{localidade: "Staten Island"},{localidade: "Queens" },{localidade:"Bronx"},{localidade: "Broklyn" }]},{_id:0,nome:1,restaurant_id:1,gastronomia:1,localidade:1}).pretty()

    #13
        > db.rest.find({ $nor: [ {"grades.score" : { $gte: 3 } }]},{_id:0,nome:1,gastronomia:1,localidade:1,"grades.score":1}).pretty()

    #14
        > db.rest.find({ $and: [  { "grades.score" : 10 } , { "grades.grade" : "A" } , { "grades.date" : new ISODate("2014-08-11")} ] },{_id:0,nome:1, grades:1}).pretty()

    // score: { "grades.score" : 10 }
    // grade: { "grades.grade" : "A" }
    // date : { "grades.date" : new ISODate("2014-08-11")}

    #15
        > db.rest.find({ $and: [{ "grades.1.grade" : "A" } , { "grades.1.date" : new ISODate("2014-08-11")} ] },{_id:0,nome:1, "grades.score":1}).pretty()

        // db.rest.find({ "grades.1.grade": "A" }).pretty()
        // db.rest.find({ "grades.1.date": new ISODate("2014-08-11") }).pretty()

    #16
        > db.rest.find( { "address.coord.1" : { $gt: 42 , $lte: 52 } },{_id:0, restaurant_id:1, nome:1, address :1 } ).pretty()

    #17
        > db.rest.find({},{_id:0,nome:1}).sort( {nome: 1 } ).pretty()

    #18
        > db.rest.find({},{_id:0,nome:1,restaurant_id:1,gastronomia:1,localidade:1}).sort( { gastronomia:1, localide: -1 }).pretty()

*   #19
        > db.rest.find({ $and : [ { localidade:"Brooklyn }, { gastronomia: { $ne : "American" } } ] },{_id:0, nome:1, restaurant_id:1, grades:1, gastronomia:1,localidade:1} ).sort( { gastronomia: -1 } ).pretty()

    #20
        > db.rest.aggregate({$group : { _id : "$localidade", count : {$sum : 1}}})
        // { "_id" : "Bronx", "count" : 309 }
        // { "_id" : "Manhattan", "count" : 1883 }
        // { "_id" : "Brooklyn", "count" : 684 }
        // { "_id" : "Staten Island", "count" : 158 }
        // { "_id" : "Queens", "count" : 738 }

    #21
        > db.rest.distinct("nome", { "grades.score" : { $gt: 30 } })

    #22
        > db.rest.aggregate([ { $match:   {  "address.coord.0" : { $lt: -65 } } }, { $group:   {   _id: "$nome", total :{ $sum : { $sum : "$grades.score" } } } }, { $match:   { total : { "$gt": 75 } } }]).pretty()

        // db.rest.aggregate([ { $match:   {  "address.coord.0" : { $lt: -65 } } },
        //                     { $group:   {   _id: "$nome",
        //                                     total :{ $sum : { $sum : "$grades.score" } }
        //                                 }
        //                     },
        //                     { $match:   { total : { "$gt": 75 } } }
        //                   ]).pretty()

    #23
        > db.rest.aggregate([ {$group: { _id : "$gastronomia", count: { $sum : { $sum : 1 } } } }, { $sort: { count: -1 } }])
    
    #24
        > db.rest.distinct( "gastronomia" ,{ "address.rua" : "Flatbush Avenue" } ).length

    #25
        > db.rest.aggregate([ { "$group": { "_id": { "rua": "$address.rua" } , "count":{ $sum : { $sum : 1 } } } },{ $sort : { count: -1 } }])

    #26
        (...)