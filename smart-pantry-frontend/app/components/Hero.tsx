export default function Hero() {
  return (
    <section className="bg-black text-white py-24 px-8 text-center">
      <h1 className="text-5xl font-bold mb-6">
        Cook smarter with{" "}
        <span className="text-yellow-500">AI-powered</span> recipes
      </h1>

      <p className="text-gray-400 max-w-2xl mx-auto">
        Enter your ingredients and let our AI chef create personalized recipes
        tailored to what you have on hand.
      </p>
    </section>
  );
}