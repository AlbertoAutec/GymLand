#qui introduremmo il nostro schema Marshmallow per validare i dati degli articoli
#in cosa consiste il nostro schema Marshmallow per gli articoli: in pratica, definisce i campi che un articolo deve avere e le loro proprietà

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class TrainerSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    nome = fields.Str()
    cognome = fields.Str()

class SupervisorSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    nome = fields.Str()
    cognome = fields.Str()

class EsercizioSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    descrizione = fields.Str()
    immagine = fields.Str()

class SchedaSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    trainer_id = fields.Int(required=True)
    validita_inizio = fields.Date()
    validita_fine = fields.Date()
    descrizione = fields.Str()
    esercizi = fields.List(fields.Nested(EsercizioSchema))
