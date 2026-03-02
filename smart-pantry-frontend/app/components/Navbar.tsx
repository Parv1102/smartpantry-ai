export default function Navbar() {
  return (
    <nav className="w-full bg-black text-white px-8 py-4 flex justify-between items-center">
      <h1 className="text-xl font-bold text-yellow-400">
        🍳 Smart Pantry
      </h1>

      <div className="space-x-6">
        <button className="hover:text-yellow-400">Home</button>
        <button className="bg-yellow-500 text-black px-4 py-1 rounded-md font-medium">
          Sign In
        </button>
      </div>
    </nav>
  );
}