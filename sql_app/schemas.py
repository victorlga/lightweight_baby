from pydantic import BaseModel, EmailStr, Field

class PlanBase(BaseModel):
    """
    Gym's plans are subscription options available for gym's members.

    Each plan can be subscribed by lots of members.

    To delete a plan, first it is necessary to update or delete members whose plan is being deleted.
    """

    name: str = Field(default=..., 
                      examples=["PlanoHard"],
                      title="Plan's name",
                      max_length=20)
    
    value: float = Field(default=...,
                         examples=[35.4],
                         title="Plan's value", 
                         description="Gym's monthly subscription plan value in reais.")
    
    description: str = Field(default=None,
                             examples=["plano para usuários de trembolona"],
                             title="Plan's description", 
                             description="Gym's monthly subscription plan description. Explain here plan's conditions, service level agreement and benefits.",
                             max_length=200
                             )


class PlanCreate(PlanBase):
    pass

class PlanUpdate(PlanBase):
    pass


class Plan(PlanBase):
    ID : int = Field(default=..., 
                     examples=[1],
                     title="Plan's ID",
                     ge=0)
    
    class Config:
        from_attributes = True

#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################

class MemberBase(BaseModel):
    """
    Gym's members are people who pay for one of the gym's subscription plan.

    Each member can subscribe to just one subscription plan.

    Every member must be subscribed to some plan.
    """

    first_name: str = Field(default=None,
                            examples=["João"],
                            title="Member's first name",
                            max_length=20)
    last_name: str = Field(default=None, 
                           examples=["Dos Venenos"],
                           title="Member's last name",
                           max_length=20)
    email: EmailStr = Field(default=...,
                            examples=["joao@testoAquosa.com"],
                            title="Member's e-mail",
                            description="Format: [email_name]@[email_domain]",
                            max_length=50)
    plan_id: int = Field(default=..., 
                         title="Member's plan",
                         examples=[0],
                         ge=0)


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
    pass

class Member(MemberBase):
    ID : int = Field(default=..., 
                     title="Member's ID",
                     examples=[1],
                     ge=0)
    
    class Config:
        from_attributes = True
