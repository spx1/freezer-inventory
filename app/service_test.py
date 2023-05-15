from .model import CCategory, CItem
from .interface import CategoryInterface, ItemInterface
from .service import CategoryService, ItemService
import pytest
from .fixtures import app, db

@pytest.fixture()
def categories(db):
    categories = [
            CCategory(id=1,name="Chicken"),
            CCategory(id=2,name="Beef")
    ]
    for category in categories:
        db.session.add(category)

    db.session.commit()
    return categories

class TestCategoryService:
    def test_create(self,db):
        test_category = CategoryInterface(id=2, name="Chicken")
        CategoryService.create(test_category)

        categories = CCategory.query.all()
        assert len(categories) == 1
        category=categories[0]
        for k in test_category.keys():
            assert getattr(category,k) == test_category[k]

    def test_get(self,categories):
        """Test search by ID & search by name"""
        test_interfaces = [
            ( CategoryInterface(id=categories[0].id) , categories[0] ),
            ( CategoryInterface(name=categories[1].name) , categories[1] ),
            ( CategoryInterface(id=categories[0].id,name=categories[1].name) , categories[0] )
        ]

        for test_interface, test_category in test_interfaces:
            comparison = CategoryService.get(test_interface)
            assert len(comparison) == 1 , f"{test_interface['id']},{test_interface['name']}"
            for k in comparison[0].keys():
                assert getattr(test_category,k) == comparison[0][k]

        """ Test invalid id passed"""
        test_interfaces = [
            CategoryInterface(id=9999),
            CategoryInterface(name='Not Used')
        ]
        for test_interface in test_interfaces:
            comparison = CategoryService.get(test_interface)
            assert len(comparison) == 0

        """ Return all categories if None is passed"""
        test_interfaces = [
            None,
            CategoryInterface(id=-1)
        ]
        for test_interface in test_interfaces:
            comparison = CategoryService.get()
            assert len(comparison) == len(categories)

