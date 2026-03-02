from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


# --- Ingredient Input Schema ---

class GenerateRecipeRequest(BaseModel):
    ingredients: List[str] = Field(
        ..., 
        example=["chicken", "garlic", "rice"]
    )
    dietary_preferences: Optional[List[str]] = Field(
        default=None,
        example=["vegetarian", "low-carb"]
    )
    max_prep_time: Optional[int] = Field(
        default=None,
        example=30
    )


# --- Step Schema ---

class StepResponse(BaseModel):
    step_number: int
    instruction: str


# --- Recipe Response Schema ---

class RecipeResponse(BaseModel):
    id: UUID
    title: str
    description: str
    prep_time_minutes: int
    cook_time_minutes: int
    difficulty: str
    calories: Optional[int]
    ingredients: List[str]
    tags: List[str]
    steps: List[StepResponse]


# --- Simple Health Schema (Optional future use) ---

class HealthResponse(BaseModel):
    status: str