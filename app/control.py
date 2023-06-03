from flask import Blueprint,render_template,redirect,url_for
from app import TEMPLATE_DIRECTORY, STATIC_DIRECTORY, APP_NAME
from .service import ItemService, CategoryService
from .interface import ItemInterface, CategoryInterface
from .schema import ItemSchema, CategorySchema
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField
from wtforms.validators import DataRequired,Optional

api = Blueprint(
    name = f'{APP_NAME}',
    import_name = __name__,
    static_folder= STATIC_DIRECTORY,
    template_folder=TEMPLATE_DIRECTORY,
    url_prefix = f'/{APP_NAME}'
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
    items = ItemService.get()
    form = MyForm()

    return render_template('inventory.html',items=items, form=form)

@api.route(rule='/items', methods=['POST'])
def post_item():
    form = MyForm()
    print(form.get_interface())
    if form.validate_on_submit():
        print(form.get_interface())
        ItemService.create(form.get_interface())
    
    return redirect(url_for(f'{APP_NAME}.get_application_page'))

