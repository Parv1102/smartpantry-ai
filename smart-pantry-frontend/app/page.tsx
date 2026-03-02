import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import IngredientInput from "./components/IngredientInput";

export default function Home() {
  return (
    <main className="min-h-screen bg-black">
      <Navbar />
      <Hero />
      <IngredientInput />
    </main>
  );
}