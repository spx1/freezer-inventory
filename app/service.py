from .interface import CategoryInterface, ItemInterface
from .model import CCategory, CItem
from app import db
from typing import List,Iterator,Dict
import datetime


class CategoryService:
    @staticmethod
    def create(obj : CategoryInterface) -> List[CategoryInterface]:
        """Create a Category Instance based on the information passed by obj"""
        def validate(obj : CategoryInterface) -> bool:
            if obj.get('id') is not None:
                if obj['id'] < 0: 
                    raise ValueError(f"CCategory 'id'={obj['id']}, expected empty or value greater than 0")
                if CCategory.query.filter(CCategory.id==obj['id']).count() > 0: 
                    raise ValueError(f"CCategory 'id'={obj['id']}, which is already in use")
            if obj.get('name',"") == "": 
                raise ValueError(f"CCategory create requires a name but none was provided")
            if CCategory.query.filter(CCategory.name==obj['name']).count() > 0: 
                raise ValueError(f"CCategory create expects a unuique name but '{obj['name']}' is already in use")
            return True;   
        
        try:
            validate(obj)
            db.session.add(CCategory( **obj ))
            db.session.commit()
            return CategoryService.get(obj)
        except ValueError as e:
            print(e)
            return []


    @staticmethod
    def get(obj : CategoryInterface = None) -> List[CategoryInterface]:
        """Get a list of objects that match the search criteria"""
        def CCategoryList2InterfaceList(objs:List[CCategory]):
            def CCategory2Interface(obj:CCategory):
                return CategoryInterface(id=obj.id, name=obj.name)
            return [CCategory2Interface(x) for x in objs]

        query = CCategory.query
        if obj is not None:
            if obj.get('id') is not None and obj.get('id') >= 0:
                query = query.filter(CCategory.id == obj['id'])
            elif obj.get('name',"") != "":
                query = query.filter(CCategory.name.like( obj.get('name','%') ) )
        return CCategoryList2InterfaceList( query.order_by(CCategory.name).all() )
    
    @staticmethod
    def get_or_create(id : int = None, obj : CategoryInterface = None ) -> CategoryInterface:
        search : CategoryInterface
        if obj is not None:
            search = CategoryInterface(
                id=obj.get('id'),
                name = obj.get('name', 'Unknown')
            )
        else:
            search = CategoryInterface(id=id,name='Unknown')

        categories = CategoryService.get(search)
        if len(categories) > 0:
            return categories[0]
        else:
            return CategoryService.create(search)[0]        


class ItemService:
    @staticmethod
    def create(obj : ItemInterface) -> List[ItemInterface]:
        def validate(obj : ItemInterface) -> bool:
            if 'id' in obj:
                if obj['id'] < 0:
                    raise ValueError(f"CItem 'id'={obj['id']}, expected empty or value greater than 0")
                if CItem.query.filter(CItem.id==obj['id']).count() > 0:
                    raise ValueError(f"CCategory 'id'={obj['id']}, which is already in use")       
        
        try:
            validate(obj)
            category = CategoryService.get_or_create(obj.get('category_id'),obj.get('category'))
            #obj['category'] = category
            obj['category_id'] = category['id']
            obj.pop('category')
            if 'added' not in obj: obj['added'] = datetime.datetime.now().date()
            db.session.add(CItem( **obj ))
            db.session.commit()
            return ItemService.get(obj)
        except ValueError as e:
            print(e)
            return []
        
    @staticmethod
    def get_object(filter : ItemInterface = None) -> List[CItem]:
        query = CItem.query.join(CCategory)
        if filter is not None:
            if 'active' in filter:
                query = query.filter(CItem.active == filter['active'])
            if 'id' in filter and filter['id'] >= 0:
                query = query.filter(CItem.id == filter['id'])
            else:
                query = query.filter( CItem.name.like( filter.get('name','%') ) )
                if 'category_id' in filter:
                    query = query.filter(CItem.category_id == filter['category_id'])
                elif 'category' in filter:
                    category = filter['category']
                    if 'id' in category:
                        query = query.filter(CCategory.id == category['id'])
                    else:
                        query = query.filter(CCategory.name.like( category.get('name','%') ) )
        return query.order_by(CItem.added).all()
    
    @staticmethod    
    def get(filter : ItemInterface = None, unique : bool = False) -> List[ItemInterface]:
        def CItemList2InterfaceList(objs:List[CItem]):
            def CItem2Interface(obj:CItem):
                return ItemInterface(
                    id=obj.id, name=obj.name, category_id=obj.category_id,
                    category = obj.category, weight=obj.weight, count=obj.count,
                    active=obj.active, added=obj.added, removed=obj.removed
                    )
            return [CItem2Interface(x) for x in objs]
        
        items = ItemService.get_object(filter)
        if unique:
            # remove duplicate name/cateogry items by creating a dictionary key from them
            dict : Dict[str,CItem] = {f"{x.name}:{x.category.name}" : x for x in items}
            items = dict.values()
        return CItemList2InterfaceList( items )
    
    @staticmethod
    def get_name_match(token : str, limit : int = 5, category : CategoryInterface = None ) -> List[str]:
        from sqlalchemy import select, func, desc
        if len(token) < 2 : return []
        # SELECT name, count(name) AS Count WHERE .... GROUP BY name ORDER BY Count
        stmt = select(CItem.name, func.count(CItem.name).label("name_count")) \
                .filter(CItem.name.like(f"%{token}%"))              
        
        if category is not None:
            stmt = stmt.filter(CItem.category_id == category.id)
        
        stmt = stmt.group_by(CItem.name) \
                .order_by(desc("name_count"), CItem.name) \
                .limit(limit)

        result = db.session.execute(stmt)
        matches = [x for x, in result.columns('name')]
        return matches

    @staticmethod
    def update(item: ItemInterface, updates: ItemInterface) -> ItemInterface:
        obj = ItemService.get_object(item)[0]

        for key in updates.keys():
            setattr(obj, key, updates[key])

        if 'active' in updates and not updates['active'] and 'removed' not in updates:
            obj.removed = datetime.datetime.now().date()

        db.session.commit()

        return ItemService.get( ItemInterface(id=obj.id) )[0]

