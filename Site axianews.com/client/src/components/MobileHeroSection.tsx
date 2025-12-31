/*
 * MOBILE HERO SECTION COMPONENT - Clone Globo.com
 * Design: Layout mobile idêntico ao Globo.com
 * 
 * Estrutura:
 * 1. Manchete principal (texto vermelho grande)
 * 2. Duas notícias secundárias (bullets)
 * 3. Card de notícia com foto e caixa de texto vermelha sobreposta
 */

interface MainNews {
  title: string;
  bullets: string[];
}

interface PhotoNews {
  title: string;
  image: string;
  bullet?: string;
}

interface MobileHeroSectionProps {
  mainNews: MainNews;
  photoNews: PhotoNews;
}

export default function MobileHeroSection({
  mainNews,
  photoNews,
}: MobileHeroSectionProps) {
  return (
    <section className="lg:hidden bg-white">
      {/* Main News - Text Only */}
      <div className="px-4 py-5">
        <h1 
          className="text-2xl sm:text-3xl font-bold leading-tight mb-4"
          style={{ 
            fontFamily: "'Encode Sans Semi Condensed', sans-serif",
            color: '#FF0000'
          }}
        >
          {mainNews.title}
        </h1>

        {/* Secondary News Bullets */}
        <div className="space-y-3 border-t border-gray-100 pt-4">
          {mainNews.bullets.map((bullet, index) => (
            <a 
              key={index}
              href="#"
              className="flex items-start gap-3 group"
            >
              <span 
                className="w-2 h-2 rounded-full mt-2 flex-shrink-0"
                style={{ backgroundColor: '#FF0000' }}
              />
              <span className="text-base text-gray-800 group-hover:text-gray-600 transition-colors leading-snug">
                {bullet}
              </span>
            </a>
          ))}
        </div>
      </div>

      {/* Photo News Card */}
      <div className="px-4 pb-6">
        <a href="#" className="block group">
          <div className="relative overflow-hidden rounded-2xl shadow-lg">
            {/* Image */}
            <img
              src={photoNews.image}
              alt={photoNews.title}
              className="w-full aspect-[4/3] object-cover"
            />
            
            {/* Red Text Box Overlay */}
            <div 
              className="absolute bottom-0 left-0 right-0 p-4 sm:p-5"
              style={{ backgroundColor: '#E41E26' }}
            >
              <h2 
                className="text-lg sm:text-xl font-bold text-white leading-tight"
                style={{ fontFamily: "'Encode Sans Semi Condensed', sans-serif" }}
              >
                {photoNews.title}
              </h2>
            </div>
          </div>
        </a>

        {/* Photo News Bullet */}
        {photoNews.bullet && (
          <div className="mt-4">
            <a 
              href="#"
              className="flex items-start gap-3 group"
            >
              <span 
                className="w-2 h-2 rounded-full mt-2 flex-shrink-0"
                style={{ backgroundColor: '#FF0000' }}
              />
              <span className="text-base text-gray-800 group-hover:text-gray-600 transition-colors leading-snug">
                {photoNews.bullet}
              </span>
            </a>
          </div>
        )}
      </div>
    </section>
  );
}
