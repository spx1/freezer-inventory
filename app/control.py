from flask import Blueprint,render_template
from app import TEMPLATE_DIRECTORY, STATIC_DIRECTORY, APP_NAME
from .service import ItemService, CategoryService
from .interface import ItemInterface, CategoryInterface
from .schema import ItemSchema, CategorySchema

api = Blueprint(
    name = f'{APP_NAME}',
    import_name = __name__,
    static_folder= STATIC_DIRECTORY,
    template_folder=TEMPLATE_DIRECTORY,
    url_prefix = f'/{APP_NAME}'
)

@api.route(methods=['GET'])
def get_application_page():
    filters = ItemInterface(active=True)
    items = ItemService.get(filters)

    return render_template('inventory.html',items=items)

