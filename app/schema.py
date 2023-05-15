from marshmallow import Schema,fields

class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()

class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    category_id = fields.Int()
    category = fields.Nested(CategorySchema)
    weight = fields.Float()
    count = fields.Int()
    active = fields.Bool()
    added = fields.DateTime()
    removed = fields.DateTime()





