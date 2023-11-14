from enum import Enum
from fastapi import Body, FastAPI, HTTPException, Path, status
from sql_app.models import Member, Plan
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trembolona Gym API",
              description="This API is used to manage gym's members and plans. Maciel e Márcio, para ficar grande tem um segredinho: trembolona.")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Tags(Enum):
    members = "Members"
    plans = "Plans"

############################################################
#=====================view for members=====================#
############################################################

@app.get("/members",
         tags=[Tags.members.value],
         response_model=list[schemas.Member],
         response_model_exclude_unset=True,
         summary="Get all members",
         description="Returns a list with all members in dict format",
         responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: No members found in dict"}},
         )
def get_members(db: Session = Depends(get_db)):
    """
    This endpoint returns all members, it does not receive parameters.
    """
    members = crud.get_members(db)


    if members == []:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No members found in dict",
        )
    return members


@app.get("/members/{member_id}",
         tags=[Tags.members.value],
         response_model=schemas.Member,
         response_model_exclude_unset=True,
         summary="Get a member",
         description="Returns a specific member in dict format based on its ID",
         responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: Member not found in dict"}},
         )
def get_member(
    member_id: Annotated[int, Path(description="Member's ID", ge=0)],
    db: Session = Depends(get_db)
):
    """
    To retrieve information about a member it is necessary to pass the member's ID.
    """
    member = crud.get_member(db, member_id)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Member not found in dict",
        )
    return member

@app.get("/membersByName/{first_name}/{last_name}",
         tags=[Tags.members.value],
         response_model=schemas.Member,
         response_model_exclude_unset=True,
         summary="Get a member",
         description="Returns a specific member in dict format based on its name",
         responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: Member not found in dict"}},
         )
def get_member(
    first_name: Annotated[str, Path(description="Member's first name")],
    last_name: Annotated[str, Path(description="Member's last name")],
    db: Session = Depends(get_db)
):
    """
    To retrieve information about a member it is necessary to pass the member's first and last name.
    """
    member = crud.get_member_by_name(db, first_name, last_name)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Member not found in dict",
        )
    return member


@app.put("/members/{member_id}",
         tags=[Tags.members.value],
         response_model=schemas.Member,
         response_model_exclude_unset=True,
         summary="Update a member",
         description="Updates a specific member in dict format based on its ID. All of the member's fields are updated.",
         responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: Member not found in dict"},
                    status.HTTP_400_BAD_REQUEST: {"description": "Bad Request Error: empty body"},
                    status.HTTP_409_CONFLICT: {"description": "Conflict Error: Member's new plan does not exist"}},
         )
def update_member(
    member_id: Annotated[int, Path(description="Member's ID", ge=0)],
    member: Annotated[schemas.MemberUpdate, Body(description="Updated member's data",
            )] = ...,
    db: Session = Depends(get_db)
):
    """
    To update a plan it is necessary to pass all the plan's fields:

    - **ID**: will be used to identify the member
    - **first_name**: each first name should be updated
    - **last_name**: each last name should be updated
    - **email**: each email should be updated
    - **plan_id**: each plan id should be updated
    """  
    if member == ...:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields",
        )
    getMember = crud.get_member(db, member_id)
    if getMember is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Member not found in dict",
        )
    member = crud.update_member(db, member,member_id)
    getPlan = crud.get_plan(db, member.plan_id)
    if getPlan is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Member's new plan does not exist",
        )
    
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Member not found in dict",
        )
    
    return member



@app.delete("/members/{member_id}",
            tags=[Tags.members.value],
            response_model=schemas.Member,
            response_model_exclude_unset=True,
            responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: Member not found in dict"}},
            summary="Delete a member",
            description="Deletes a specific member in dict format based on its ID. The deleted member is returned.",
            )
def delete_member(
    member_id: Annotated[int, Path(description="Member's ID", ge=0)],
    db: Session = Depends(get_db)
):
    """
    To delete a member it is necessary to pass the member's ID.
    """
    getMember = crud.get_member(db, member_id)
    if getMember is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Member not found in dict",
        )
    member = crud.delete_member(db, member_id)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Member not found in dict",
        )
    
    return member


@app.post("/members",
          tags=[Tags.members.value],
          response_model=schemas.Member,
          response_model_exclude_unset=True,
          status_code=status.HTTP_201_CREATED,
          summary="Create a member",
          description="Creates a new member. The new member is returned.",
          responses={status.HTTP_409_CONFLICT: {"description": "Conflict Error: Member already exists"},
                     status.HTTP_400_BAD_REQUEST: {"description": "Bad Request Error: empty body"},
                     status.HTTP_409_CONFLICT: {"description": "No Content: Member's plan does not exist"},
          }
          )

def create_member(
    member: Annotated[
        schemas.MemberCreate,
        Body(
            description="New member's data",
            examples=[
                {
                    "first_name": "joao",
                    "last_name": "trembo",
                    "email": "joao@trembo.com",
                    "plan_id": 1,
                }
            ]
        ),
    ] = ...,
    db: Session = Depends(get_db)
):

    """
    Create a member with all the information:

    - **ID**: each member must have a unique ID
    - **first_name**: each member may have a first name
    - **last_name**: each member may have a last name
    - **email**: each member must have an email
    - **plan_id**: each member must have a plan_id
    """
    # #check if body is empty
    if member == ...:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields",
        )

    
    getPlan = crud.get_plan(db, member.plan_id)
    if getPlan is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Member's plan does not exist",
        )
    getMember = crud.get_member_by_name(db, member.first_name,member.last_name)

    if getMember != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Member already exists",
        )

    member = crud.create_member(db, member)
    return member

############################################################
##=====================view for plans=====================##
############################################################

@app.get("/plans",
         tags=[Tags.plans.value],
         response_model=list[schemas.Plan],
         response_model_exclude_unset=True,
         summary="Get all plans",
         description="Returns a list with all plans in dict format",
         responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: No plans found in dict"}},
         )
def get_plans(db: Session = Depends(get_db)):
    """
    This endpoint returns all plans, it does not receive parameters.
    """
    plans = crud.get_plans(db)
    if plans == []:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No plans found in dict",
        )
    
    return plans


@app.get("/plans/{plan_id}",
         tags=[Tags.plans.value],
         response_model=schemas.Plan,
         response_model_exclude_unset=True,
         description="Returns a specific plan in dict format based on its ID",
         summary="Get a plan",
         responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: Plan not found in dict"}},
         )
def get_plan(
    plan_id: Annotated[int, Path(description="Plan's ID", ge=0)],
    db: Session = Depends(get_db)
):
    """
    To retrieve information about a plan it is necessary to pass the plan's ID.
    """
    plan = crud.get_plan(db, plan_id)
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Plan not found in dict",
        )
    return plan

@app.get("/plansByName/{plan_name}",
         tags=[Tags.plans.value],
         response_model=schemas.Plan,
         response_model_exclude_unset=True,
         description="Returns a specific plan in dict format based on its name",
         summary="Get a plan by its name",
         responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: Plan not found in dict"}},
         )
def get_plan_by_name(
    plan_name: Annotated[str, Path(description="Plan's name")],
    db: Session = Depends(get_db)
):
    """
    To retrieve information about a plan it is necessary to pass the plan's name.
    """
    plan = crud.get_plan_by_name(db, plan_name)
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Plan not found in dict",
        )
    return plan

@app.get("/plans/{plan_id}/members",
         tags=[Tags.plans.value],
         response_model=list[schemas.Member],
         response_model_exclude_unset=True,
         description="Returns a list with all members subscribed to a specific plan in dict format based on its ID",
         summary="Get a plan's members",
         responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: Plan not found in dict"},
                    status.HTTP_204_NO_CONTENT: {"description": "No Content: Plan has no members"}},
)
def get_plan_members(
    plan_id: Annotated[int, Path(description="Plan's ID", ge=0)],
    db: Session = Depends(get_db)
):
    """
    To get all members enrolled in a plan it is necessary to pass the plan's ID.
    Plans with no members enrolled will not return users.
    """
    plan_members = crud.get_plan_members(db, plan_id)
    if plan_members == []:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Plan not found in dict",
        )


    return plan_members
    

@app.put("/plans/{plan_id}",
         tags=[Tags.plans.value],
         response_model=schemas.Plan,
         response_model_exclude_unset=True,
         description="Updates a specific plan in dict format based on its ID. All of the plan's fields are updated.",
         summary="Update a plan",
         responses={status.HTTP_204_NO_CONTENT: {"description": "No Content: Plan not found in dict"},
                    status.HTTP_400_BAD_REQUEST: {"description": "Bad Request Error: empty body"}},
         )
def update_plan(
    plan_id: Annotated[int, Path(description="Plan's ID", ge=0)],
    plan: Annotated[schemas.PlanUpdate, Body(description="Updated plan's data",examples=[
                        {
                            "name": "Plano Hard",
                            "value": 35.4,
                            "description": "plano para usuários de bomba",
                        }
                    ],)] = ...,
    db: Session = Depends(get_db)
):
    """
    To update a plan it is necessary to pass all the plan's fields:

    - **ID**: will be used to identify the plan
    - **name**: each name should be updated 
    - **value**: each value should be updated 
    - **description**: each description should be updated 
    """
    #check if body does not have necessary fields
    if plan == ...:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields",
        )
    
    getPlan = crud.get_plan(db, plan_id)

    if getPlan is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Plan not found in dict",
        )
    plan = crud.update_plan(db, plan, plan_id)
    return plan



@app.delete("/plans/{plan_id}",
            tags=[Tags.plans.value],
            response_model=schemas.Plan,
            response_model_exclude_unset=True,
            description="Deletes a specific plan in dict format based on its ID. The deleted plan is returned.",
            summary="Delete a plan",
            responses={status.HTTP_409_CONFLICT: {"description": "Conflict Error: Plan has members. First update members' plan"},
                       status.HTTP_204_NO_CONTENT: {"description": "No Content: Plan not found in dict"}},
            )
def delete_plan(
    plan_id: Annotated[int, Path(description="Plan's ID", ge=0)],
    db: Session = Depends(get_db)
):
    """
    To delete a plan, first it is necessary to update or delete members whose plan is being deleted.
    """
    
    plan_members = crud.get_plan_members(db, plan_id)
    
    if plan_members != []:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Plan has members. First update members' plan",
        )
    getPlan = crud.get_plan(db, plan_id)
    if getPlan is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Plan not found in dict",
        )
    plan = crud.delete_plan(db, plan_id)
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Plan not found in dict",
        )
    return plan


@app.post("/plans",
          tags=[Tags.plans.value],
          response_model=schemas.Plan,
          response_model_exclude_unset=True,
          status_code=status.HTTP_201_CREATED,
          responses={status.HTTP_409_CONFLICT: {"description": "Conflict Error: Plan already exists"},
                     status.HTTP_400_BAD_REQUEST: {"description": "Bad Request Error: empty body"}},
          description="Creates a new plan. The new plan is returned.",
          summary="Create a plan",
          )
def create_plan(
    plan: Annotated[
        schemas.PlanCreate, 
        Body(description="Updated plan's data",
            examples=[
                        {
                            "name": "Plano Hard",
                            "value": 35.4,
                            "description": "plano para usuários de bomba",
                        }
                    ],
         )] = ...,
    db: Session = Depends(get_db)
):
    """
    Create an plan with all the information:

    - **ID**: each plan must have a unique ID
    - **name**: each plan must have a name
    - **description**: each plan may have a description
    """
    if plan == ...:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields",
        )
    getPlan = crud.get_plan_by_name(db, plan.name)
    if getPlan != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Plan already exists",
        )
    plan = crud.create_plan(db, plan)
    return plan