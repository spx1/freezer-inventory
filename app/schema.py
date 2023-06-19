from marshmallow import Schema,fields

class CategorySchema(Schema):
    id = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)

class ItemSchema(Schema):
    id = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)
    category_id = fields.Int(allow_none=True)
    category = fields.Nested(CategorySchema,allow_none=True)
    weight = fields.Float(allow_none=True)
    count = fields.Int(allow_none=True)
    active = fields.Bool(allow_none=True)
    added = fields.DateTime(allow_none=True)
    removed = fields.DateTime(allow_none=True)





