"use client";

import { useState } from "react";

export default function IngredientInput() {
  const [ingredient, setIngredient] = useState("");
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [recipe, setRecipe] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const addIngredient = () => {
    if (!ingredient.trim()) return;
    setIngredients([...ingredients, ingredient]);
    setIngredient("");
  };

  const generateRecipe = async () => {
    if (ingredients.length === 0) return;

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/recipes/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ingredients }),
      });

      const data = await response.json();
      setRecipe(data);
    } catch (error) {
      console.error("Error generating recipe:", error);
    }

    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto mt-12 bg-gray-900 p-6 rounded-lg">
      <div className="flex gap-2">
        <input
          value={ingredient}
          onChange={(e) => setIngredient(e.target.value)}
          placeholder="Enter ingredient (e.g. chicken)"
          className="flex-1 px-4 py-2 rounded-md bg-gray-800 text-white"
        />
        <button
          onClick={addIngredient}
          className="bg-yellow-500 text-black px-4 rounded-md"
        >
          Add
        </button>
      </div>

      <div className="mt-4">
        {ingredients.map((ing, index) => (
          <span
            key={index}
            className="inline-block bg-gray-700 text-white px-3 py-1 mr-2 mt-2 rounded-full"
          >
            {ing}
          </span>
        ))}
      </div>

      <button
        onClick={generateRecipe}
        className="mt-6 w-full bg-green-500 text-black py-2 rounded-md font-semibold"
      >
        {loading ? "Generating..." : "Generate Recipe"}
      </button>

      {recipe && (
        <div className="mt-8 bg-gray-800 p-4 rounded-md text-white">
          <h2 className="text-xl font-bold">{recipe.title}</h2>
          <p className="text-gray-400">{recipe.description}</p>

          <h3 className="mt-4 font-semibold">Steps:</h3>
          <ul className="list-disc ml-5">
            {recipe.steps.map((step: any, index: number) => (
              <li key={index}>{step.instruction}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}