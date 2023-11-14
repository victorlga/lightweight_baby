from sqlalchemy.orm import Session

from . import models, schemas


def get_member(db: Session, member_id: int):
    member = db.query(models.Member).filter(models.Member.ID == member_id).first()
    return member


def get_member_by_name(db: Session, first_name: str,last_name: str):
    member = db.query(models.Member).filter((models.Member.first_name == first_name) and (models.Member.last_name == last_name)).first()
    return member

def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()


def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(
        first_name = member.first_name,
        last_name = member.last_name,
        email = member.email,
        plan_id = member.plan_id
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def update_member(db: Session, member: schemas.MemberUpdate, member_id: int):
    db_member = db.query(models.Member).filter(models.Member.ID == member_id).first()
    db_member.first_name = member.first_name
    db_member.last_name = member.last_name
    db_member.email = member.email
    db_member.plan_id = member.plan_id
    db.commit()
    db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int):
    db_member = db.query(models.Member).filter(models.Member.ID == member_id).first()
    db.delete(db_member)
    db.commit()
    return db_member


def get_plans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Plan).offset(skip).limit(limit).all()


def create_plan(db: Session, plan: schemas.PlanCreate):
    print 
    db_plan = models.Plan(name = plan.name, value = plan.value, description = plan.description)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_plan(db: Session, _id: int):
    return db.query(models.Plan).filter(models.Plan.ID == _id).first()

def get_plan_by_name(db: Session, name: str):
    return db.query(models.Plan).filter(models.Plan.name == name).first()

def get_plan_members(db: Session, plan_id: int):
    return db.query(models.Member).filter(models.Member.plan_id == plan_id).all()

def update_plan(db: Session, plan: schemas.Plan, plan_id: int):
    db_plan = db.query(models.Plan).filter(models.Plan.ID == plan_id).first()
    db_plan.name = plan.name
    db_plan.value = plan.value
    db_plan.description = plan.description
    db.commit()
    db.refresh(db_plan)
    return db_plan

def delete_plan(db: Session, plan_id: int):
    db_plan = db.query(models.Plan).filter(models.Plan.ID == plan_id).first()
    db.delete(db_plan)
    db.commit()
    return db_plan
