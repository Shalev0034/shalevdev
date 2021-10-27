from . import db
from .models import User,Major,Table



def createMajors():
    from .models import Major
    majors = ['אלקטרוניקה','דיפלומטיה','כימיה','אומנות','מוסיקה','פיזיקה','מדעי המחשב']
    db.session.query(Major).delete()
    for major in majors:
        create_major(major)
    db.session.commit()
    

def create_major(name):
    major = Major(name=name,keywords="")
    db.session.add(major)