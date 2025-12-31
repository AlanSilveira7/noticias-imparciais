/*
 * RECIPES SECTION COMPONENT - Clone Globo.com
 * Design: Fidelidade Editorial Clássica
 * 
 * Seção "Vai cozinhar hoje?":
 * - Cards de receitas
 */

interface Recipe {
  title: string;
  subtitle: string;
  image: string;
}

const recipes: Recipe[] = [
  {
    title: 'Maminha com manteiga temperada dá camada extra de sabor',
    subtitle: 'Para impressionar a família',
    image: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=300&fit=crop',
  },
  {
    title: 'Lagarto frio com cebola e pimentão pode ser refeição completa',
    subtitle: 'Opção versátil',
    image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop',
  },
  {
    title: 'Crocante e saboroso: veja como fazer brigadeiro de colher',
    subtitle: 'Apenas três ingredientes',
    image: 'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400&h=300&fit=crop',
  },
  {
    title: 'Uma imersão nas tradições culinárias bascas',
    subtitle: 'San Sebastián',
    image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&h=300&fit=crop',
  },
];

export default function RecipesSection() {
  return (
    <section className="bg-gray-50 py-8">
      <div className="container">
        {/* Header */}
        <h2 
          className="text-2xl font-bold mb-6"
          style={{ 
            fontFamily: "'Encode Sans Semi Condensed', sans-serif",
            color: '#4CAF50'
          }}
        >
          Vai cozinhar hoje?
        </h2>

        {/* Recipes Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {recipes.map((recipe, index) => (
            <a 
              key={index}
              href="#"
              className="group bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="relative aspect-[4/3] overflow-hidden">
                <img
                  src={recipe.image}
                  alt={recipe.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div className="p-4">
                <span className="text-xs font-semibold text-green-600">{recipe.subtitle}</span>
                <h3 
                  className="font-bold text-gray-900 mt-1 line-clamp-2 group-hover:text-green-600 transition-colors"
                  style={{ fontFamily: "'Encode Sans Semi Condensed', sans-serif" }}
                >
                  {recipe.title}
                </h3>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
