from .interface import CategoryInterface
from .model import CCategory
from app import db
from typing import List,Iterator

class CategoryService:
    @staticmethod
    

    @staticmethod
    def create(obj : CategoryInterface) -> List[CategoryInterface]:
        """Create a Category Instance based on the information passed by obj"""
        def validate(obj : CategoryInterface) -> bool:
            if 'id' in obj:
                if obj['id'] < 0: 
                    raise ValueError(f"CCategory 'id'={obj['id']}, expected empty or value greater than 0")
                if CCategory.query.filter(CCategory.id==obj['id']).count() > 0: 
                    raise ValueError(f"CCategory 'id'={obj['id']}, which is already in use")
            if 'name' not in obj: 
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
            if 'id' in obj and obj['id'] >= 0:
                query = query.filter(CCategory.id == obj['id'])
            elif 'name' in obj and obj['name'] != "":
                query = query.filter(CCategory.name == obj['name'])
        return CCategoryList2InterfaceList( query.order_by(CCategory.name).all() )

class ItemService:
    pass