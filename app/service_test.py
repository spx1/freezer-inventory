from .model import CCategory, CItem
from .interface import CategoryInterface, ItemInterface
from .service import CategoryService, ItemService
import pytest
from .fixtures import app, db
import datetime

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

@pytest.fixture()
def items(db,categories) -> CItem:
    items = [
        CItem(id=1,name="Thighs",category=categories[0],weight=2.5,active=True,added=datetime.datetime.now().date()),
        CItem(id=2,name="Tenderloin",category=categories[1],weight=0.7,active=True,added=datetime.datetime.now().date()),
        CItem(id=3,name="Chuck",category=categories[1],weight=1.2,active=True,added=datetime.datetime.now().date()),
        CItem(id=4,name="Ground",category=categories[1],weight=1,active=False,added=datetime.datetime(year=2023, month=1, day=17)),
        CItem(id=5,name="Ground",category=categories[1],weight=1,active=True,added=datetime.datetime.now().date()),
        CItem(id=6,name="Ground",category=categories[1],weight=1,active=True,added=datetime.datetime.now().date()),
    ]
    for item in items:
        db.session.add(item)

    db.session.commit()
    return items

class TestItemService:
    def test_create(self,db):
        test_category = CategoryInterface(name="Chicken")
        test_item = ItemInterface(id=2, name="Wings", category=test_category, weight=1.2)
        ItemService.create(test_item)

        items = CItem.query.all()
        assert len(items) == 1
        item = items[0]
        for k in test_item.keys():
            assert getattr(item,k) == test_item[k]

        assert item.category.id >= 0
        assert item.category_id == item.category.id
        assert item.active == True
        assert item.added == datetime.datetime.now().date()

    def test_get(self,db,items,categories):
        """Test Search by ID, Name, & Category"""
        test_items = [
            ( ItemInterface(id=items[0].id), items[0] ),
            ( ItemInterface(name=items[3].name), items[3] ),
            ( ItemInterface(category_id=categories[0].id), items[0] )
        ]

        for test_interface, test_item in test_items:
            comparison = ItemService.get(test_interface)
            assert(len(comparison) > 0) , f"{test_interface['id']}, {test_interface['name']}"
            for k in filter(lambda x : x != "category", comparison[0].keys()):
                assert getattr(test_item, k) == comparison[0][k]
        
        """Test return all items"""
        comparison = ItemService.get()
        assert len(comparison) == len(items)

        """Test return active items of the correct category"""
        comparison = ItemService.get( ItemInterface(active=True, name="Ground"))
        assert len(comparison) == 2

        """Test invalid entries all return emtpy array"""
        empty_tests = [
            ItemInterface(id=999999),
            ItemInterface(name="Not a name"),
            ItemInterface(category_id=79)
        ]
        for empty_test in empty_tests:
            comparison = ItemService.get(empty_test)
            assert len(comparison) == 0

        """Test complex query"""
        item = items[2]
        test_interface = ItemInterface(name=item.name, category=CategoryInterface(name = item.category.name), active=True)
        comparison = ItemService.get(test_interface)

        for k in filter(lambda x : x != "category", comparison[0].keys()):
            assert getattr(item, k) == comparison[0][k]

        """Test wildcard matches on name"""
        test_interface = ItemInterface(name="Ch%", active=True)
        comparison = ItemService.get(test_interface)

        assert len(comparison) == 1
        ids = [x['id'] for x in comparison]
        assert  items[2].id in ids

        """Test wildcard matches on category name"""
        test_interface = ItemInterface(category=CategoryInterface(name="Ch%"))
        comparison = ItemService.get(test_interface)

        assert len(comparison) == 1
        ids = [x['id'] for x in comparison]
        assert  items[0].id in ids

        test_interface = ItemInterface(category=CategoryInterface(name='%ee%'))
        comparison = ItemService.get(test_interface)

        assert len(comparison) == 5
        assert items[0] not in comparison
 
    def test_get_name_matches(self,db,items,categories):
        """Test searching for names"""
        names = ItemService.get_name_match("nd")
        assert names[0] == "Ground"
        assert names[1] == "Tenderloin"

        """Test limiting the number of matches"""
        names = ItemService.get_name_match("nd",limit=1)
        assert len(names) == 1

        """Test limiting the category of the name match"""
        names = ItemService.get_name_match("gh",category=categories[1])
        assert len(names) == 0

    def test_put_item(self,db,items,categories):
        """Test renaming the device"""
        item = ItemService.get( ItemInterface(id=1) )[0]
        updates = ItemInterface(name="New Name")
        ItemService.update(item, updates)
        test = ItemService.get( item )[0]

        assert test['name'] == 'New Name'

        """ Test deactivating device"""
        item = ItemService.get( ItemInterface(id=2) )[0]
        updates = ItemInterface(active=False)
        test = ItemService.update(item, updates)
        
        assert not test['active']
        assert test['removed'] == datetime.datetime.now().date()

    def test_get_unique_item(self, db, items, categories):
        """Test that we can filter for unique name/category items"""
        item = items[5]
        tests = ItemService.get( ItemInterface(name=item.name, category=CategoryInterface(name=item.category.name)), True)
        assert len(tests) == 1

    def test_ordered_sort(self, db, items, categories):
        """Test that the sort is deterministic when given several items"""
        expected_order = [
            items[3],
            items[2],
            items[4],
            items[5],
            items[1],
            items[0]
        ]
        tests = ItemService.get( )
        print(tests)
        for e, t in zip(expected_order, tests):
            assert e.id == t['id']