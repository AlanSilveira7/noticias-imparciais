/*
 * TV SCHEDULE SECTION COMPONENT - Clone Globo.com
 * Design: Fidelidade Editorial Clássica
 * 
 * Seção "Hoje na TV Globo":
 * - Programação atual
 * - Cards de programas
 */

interface Program {
  type: string;
  title: string;
  time: string;
  image: string;
  isLive?: boolean;
}

const programs: Program[] = [
  {
    type: 'Novela',
    title: 'Dona de Mim',
    time: '10:40 PM',
    image: 'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?w=300&h=200&fit=crop',
    isLive: true,
  },
  {
    type: 'Jornalismo',
    title: 'Jornal Nacional',
    time: '11:30 PM',
    image: 'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=300&h=200&fit=crop',
  },
  {
    type: 'Novela',
    title: 'Três Graças',
    time: '12:20 AM',
    image: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=300&h=200&fit=crop',
  },
];

export default function TVScheduleSection() {
  return (
    <section className="bg-white py-8">
      <div className="container">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 
            className="text-2xl font-bold"
            style={{ 
              fontFamily: "'Encode Sans Semi Condensed', sans-serif",
              color: '#E91E63'
            }}
          >
            Hoje na TV Globo
          </h2>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-500">horário de Brasília</span>
            <a 
              href="#" 
              className="text-sm font-semibold text-pink-600 hover:underline"
            >
              Confira a programação completa
            </a>
          </div>
        </div>

        {/* Programs Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {programs.map((program, index) => (
            <a 
              key={index}
              href="#"
              className="group flex gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="relative w-24 h-16 flex-shrink-0 overflow-hidden rounded">
                <img
                  src={program.image}
                  alt={program.title}
                  className="w-full h-full object-cover"
                />
                {program.isLive && (
                  <div className="absolute top-1 left-1 px-1.5 py-0.5 bg-red-600 text-white text-[10px] font-bold rounded">
                    AGORA NO GLOBOPLAY
                  </div>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <span className="text-xs font-semibold text-pink-600">{program.type}</span>
                <p className="text-xs text-gray-500 mt-0.5">Hoje, {program.time}</p>
                <h3 
                  className="font-bold text-gray-900 mt-1 group-hover:text-pink-600 transition-colors"
                  style={{ fontFamily: "'Encode Sans Semi Condensed', sans-serif" }}
                >
                  {program.title}
                </h3>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
