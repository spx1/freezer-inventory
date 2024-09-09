from flask import Blueprint,render_template,redirect,url_for,request
from app import TEMPLATE_DIRECTORY, STATIC_DIRECTORY, APP_NAME, BASE_DIRECTORY
from .service import ItemService, CategoryService
from .interface import ItemInterface, CategoryInterface
from .schema import ItemSchema, CategorySchema
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField
from wtforms.validators import DataRequired,Optional
from typing import List

api = Blueprint(
    name = f'{APP_NAME}',
    import_name = __name__,
    static_folder= 'static',
    static_url_path='static',
    template_folder=TEMPLATE_DIRECTORY,
    url_prefix = f'/{APP_NAME}',
    root_path= BASE_DIRECTORY

)

class MyForm(FlaskForm):
    category = StringField('cateogry',validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    weight = FloatField('weight',validators=[Optional()])
    count = IntegerField('count',validators=[Optional()])

    def get_interface(self) -> ItemInterface:
        return ItemInterface(
            name = self.name.data,
            category = CategoryInterface(name = self.category.data ),
            weight = self.weight.data,
            count = self.count.data
        )
    
@api.route(rule='/home', methods=['GET'])
def get_application_page():
    filters = ItemInterface(active=True)
    items = ItemService.get(filters)
    form = MyForm()

    return render_template('inventory.html',items=items, form=form)

@api.route(rule='/items', methods=['POST'])
def post_item():
    def create():
        form = MyForm()
        print(form.get_interface())
        if form.validate_on_submit():
            print(form.get_interface())
            ItemService.create(form.get_interface())

    def copy():
        id = request.args.get("id", type=int)
        orig = ItemService.get_object( ItemInterface( id=id ) )[0]
        new = ItemInterface( 
            name = orig.name
            , category_id = orig.category_id
            , weight = orig.weight
            , count = orig.count
        )
        ItemService.create( new )
    
    if request.args.get("action",type=str, default="create") == "copy":
        copy()
    else:
        create()
    return redirect(url_for(f'{APP_NAME}.get_application_page'))

@api.route(rule='/item/<int:id>',methods=['PUT'])
def put_item(id: int):
    item = ItemService.get( ItemInterface(id=id) )[0]
    updates : ItemInterface = ItemSchema().loads(request.data)
    ItemService.update( item, updates )

    return "OK"

@api.route(rule='/items', methods=['GET'])
def get_item():
    schema = ItemSchema()
    filter = ItemInterface( 
        category = CategoryInterface(name = request.args.get("category","%") ),  
        name = request.args.get("name","%"),
        active = bool(request.args.get("active", "True"))
        )
    filter['Active'] = True
    items : List[ItemInterface] = ItemService.get(filter, request.args.get("unique", False, bool))

    return schema.dumps(items, many=True)

@api.route(rule='/categories', methods=['GET'])
def get_category():
    schema = CategorySchema()
    filter = CategoryInterface(
        name = request.args.get("category", "%")
    )
    categories : List[CategoryInterface] = CategoryService.get(filter)

    return schema.dumps(categories, many=True)