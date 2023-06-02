from marshmallow import Schema,fields

class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()

class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    category_id = fields.Int()
    category = fields.Nested(CategorySchema)
    weight = fields.Float(allow_none=True)
    count = fields.Int(allow_none=True)
    active = fields.Bool()
    added = fields.DateTime()
    removed = fields.DateTime(allow_none=True)





