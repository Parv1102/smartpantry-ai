from database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    ForeignKey,
    Table,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime


# --- Association Tables (Many-to-Many) ---

recipe_ingredients = Table(
    "recipe_ingredients",
    Base.metadata,
    Column("recipe_id", UUID(as_uuid=True), ForeignKey("recipes.id")),
    Column("ingredient_id", UUID(as_uuid=True), ForeignKey("ingredients.id"))
)

recipe_tags = Table(
    "recipe_tags",
    Base.metadata,
    Column("recipe_id", UUID(as_uuid=True), ForeignKey("recipes.id")),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"))
)


# --- Main Tables ---

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    prep_time_minutes = Column(Integer, nullable=False)
    cook_time_minutes = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)
    calories = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingredients = relationship(
        "Ingredient",
        secondary=recipe_ingredients,
        back_populates="recipes"
    )

    tags = relationship(
        "Tag",
        secondary=recipe_tags,
        back_populates="recipes"
    )

    steps = relationship("Step", back_populates="recipe", cascade="all, delete")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

    recipes = relationship(
        "Recipe",
        secondary=recipe_ingredients,
        back_populates="ingredients"
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

    recipes = relationship(
        "Recipe",
        secondary=recipe_tags,
        back_populates="tags"
    )


class Step(Base):
    __tablename__ = "steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    step_number = Column(Integer, nullable=False)
    instruction = Column(Text, nullable=False)

    recipe = relationship("Recipe", back_populates="steps")