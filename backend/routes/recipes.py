from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Recipe, Ingredient, Tag, Step
from schemas import GenerateRecipeRequest, RecipeResponse, StepResponse

router = APIRouter(prefix="/recipes", tags=["Recipes"])


# -------------------------------
# Generate Recipe (Mock Version)
# -------------------------------
@router.post("/generate", response_model=RecipeResponse)
def generate_recipe(request: GenerateRecipeRequest, db: Session = Depends(get_db)):

    new_recipe = Recipe(
        title="Custom Pantry Recipe",
        description=f"A recipe made using: {', '.join(request.ingredients)}",
        prep_time_minutes=15,
        cook_time_minutes=20,
        difficulty="Easy",
        calories=450,
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    # Add ingredients
    ingredient_objects = []
    for ingredient_name in request.ingredients:
        ingredient = db.query(Ingredient).filter_by(name=ingredient_name).first()
        if not ingredient:
            ingredient = Ingredient(name=ingredient_name)
            db.add(ingredient)
            db.commit()
            db.refresh(ingredient)

        ingredient_objects.append(ingredient)

    new_recipe.ingredients = ingredient_objects

    # Add basic steps
    steps_data = [
        "Prepare all ingredients.",
        "Cook ingredients together.",
        "Serve and enjoy."
    ]

    for i, instruction in enumerate(steps_data, start=1):
        step = Step(
            recipe_id=new_recipe.id,
            step_number=i,
            instruction=instruction
        )
        db.add(step)

    db.commit()

    return RecipeResponse(
        id=new_recipe.id,
        title=new_recipe.title,
        description=new_recipe.description,
        prep_time_minutes=new_recipe.prep_time_minutes,
        cook_time_minutes=new_recipe.cook_time_minutes,
        difficulty=new_recipe.difficulty,
        calories=new_recipe.calories,
        ingredients=[ing.name for ing in ingredient_objects],
        tags=[],
        steps=[
            StepResponse(
                step_number=i + 1,
                instruction=steps_data[i]
            )
            for i in range(len(steps_data))
        ],
    )


# -------------------------------
# Get All Recipes
# -------------------------------
@router.get("/", response_model=List[RecipeResponse])
def get_all_recipes(
    ingredient: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Recipe)

    # If ingredient filter is provided
    if ingredient:
        query = query.join(Recipe.ingredients).filter(
            Ingredient.name.ilike(f"%{ingredient}%")
        )

    recipes = query.all()

    result = []

    for recipe in recipes:
        result.append(
            RecipeResponse(
                id=recipe.id,
                title=recipe.title,
                description=recipe.description,
                prep_time_minutes=recipe.prep_time_minutes,
                cook_time_minutes=recipe.cook_time_minutes,
                difficulty=recipe.difficulty,
                calories=recipe.calories,
                ingredients=[ing.name for ing in recipe.ingredients],
                tags=[tag.name for tag in recipe.tags],
                steps=[
                    StepResponse(
                        step_number=step.step_number,
                        instruction=step.instruction
                    )
                    for step in recipe.steps
                ],
            )
        )

    return result

# -------------------------------
# Get Recipe By ID
# -------------------------------
@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe_by_id(recipe_id: UUID, db: Session = Depends(get_db)):

    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return RecipeResponse(
        id=recipe.id,
        title=recipe.title,
        description=recipe.description,
        prep_time_minutes=recipe.prep_time_minutes,
        cook_time_minutes=recipe.cook_time_minutes,
        difficulty=recipe.difficulty,
        calories=recipe.calories,
        ingredients=[ing.name for ing in recipe.ingredients],
        tags=[tag.name for tag in recipe.tags],
        steps=[
            StepResponse(
                step_number=step.step_number,
                instruction=step.instruction
            )
            for step in recipe.steps
        ],
    )