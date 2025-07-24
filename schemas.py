#qui introduremmo il nostro schema Marshmallow per validare i dati degli articoli
#in cosa consiste il nostro schema Marshmallow per gli articoli: in pratica, definisce i campi che un articolo deve avere e le loro proprietà
from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)  # ora l'id è solo in output
    name = fields.Str(required=True)  #qui definiamo il campo 'name' come stringa e lo rendiamo obbligatorio
    price = fields.Float(required=True)  #qui definiamo il campo 'price' come float e lo rendiamo obbligatorio
   
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)  # ora l'id è solo in output
    name = fields.Str()  #qui definiamo il campo 'name' come stringa e lo rendiamo obbligatorio

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)  # ora l'id è solo in output
    name = fields.Str()  #qui definiamo il campo 'name' come stringa e lo rendiamo obbligatorio

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)  #qui definiamo il campo 'items' come una lista di oggetti nidificati dello schema ItemSchema e lo rendiamo solo in output    
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)  #qui definiamo il campo 'tags' come una lista di oggetti nidificati dello schema TagSchema e lo rendiamo solo in output    

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)  #qui definiamo il campo 'store_id' come intero e lo rendiamo obbligatorio
    store = fields.Nested(PlainStoreSchema(), dump_only=True)  #qui definiamo il campo 'store' come un oggetto nidificato dello schema StoreSchema e lo rendiamo solo in output
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)  #qui definiamo il campo 'items' come una lista di oggetti nidificati dello schema ItemSchema e lo rendiamo solo in output    

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)  #qui definiamo il campo 'store_id' come stringa e lo rendiamo obbligatorio
    store = fields.Nested(PlainStoreSchema(), dump_only=True)  #qui definiamo il campo 'store' come un oggetto nidificato dello schema StoreSchema e lo rendiamo solo in output
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)  #qui definiamo il campo 'tags' come una lista di oggetti nidificati dello schema TagSchema e lo rendiamo solo in output    


class ItemUpdateSchema(Schema):
    name = fields.Str()  #qui definiamo il campo 'name' come stringa e lo rendiamo facoltativo
    price = fields.Float()  #qui definiamo il campo 'price' come float e lo rendiamo facoltativo
    store_id = fields.Int() #qui definiamo il campo 'store_id' come intero e lo rendiamo facoltativo

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)  #qui definiamo il campo 'items' come una lista di oggetti nidificati dello schema ItemSchema e lo rendiamo solo in output

class TagAndItemSchema(Schema):
    message = fields.Str()
    tag = fields.Nested(TagSchema())  #qui definiamo il campo 'tag' come un oggetto nidificato dello schema TagSchema e lo rendiamo obbligatorio
    item = fields.Nested(ItemSchema())  #qui definiamo il campo 'item' come un oggetto nidificato dello schema ItemSchema e lo rendiamo obbligatorio

class UserSchema(Schema):
    id = fields.Int(dump_only=True)  #qui definiamo il campo 'id' come intero e lo rendiamo solo in output
    username = fields.Str(required=True)  #qui definiamo il campo 'username' come stringa e lo rendiamo obbligatorio
    password = fields.Str(required=True, load_only=True)  #qui definiamo il campo 'password' come stringa e lo rendiamo obbligatorio, ma solo in input
