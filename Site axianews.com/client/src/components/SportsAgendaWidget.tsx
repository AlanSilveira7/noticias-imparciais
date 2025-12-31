/*
 * SPORTS AGENDA WIDGET COMPONENT - Clone Globo.com
 * Design: Fidelidade Editorial Clássica
 * 
 * Widget de agenda de jogos:
 * - Jogos de hoje
 * - Placar ao vivo
 */

interface Match {
  homeTeam: string;
  homeScore: number;
  awayTeam: string;
  awayScore: number;
  competition: string;
  status: 'live' | 'finished' | 'upcoming';
  time?: string;
}

const matches: Match[] = [
  {
    homeTeam: 'ROM',
    homeScore: 3,
    awayTeam: 'GEN',
    awayScore: 1,
    competition: 'Campeonato Italiano',
    status: 'finished',
  },
  {
    homeTeam: 'FLA',
    homeScore: 0,
    awayTeam: 'PAL',
    awayScore: 0,
    competition: 'Brasileirão',
    status: 'upcoming',
    time: '21:00',
  },
];

export default function SportsAgendaWidget() {
  return (
    <div>
      <a 
        href="#" 
        className="globo-section-title text-blue-600 hover:underline inline-block mb-3"
      >
        Agenda
      </a>
      
      <p className="text-sm text-gray-600 mb-3">Jogos de hoje</p>

      <div className="space-y-3">
        {matches.map((match, index) => (
          <div 
            key={index}
            className="p-3 bg-gray-50 rounded"
          >
            <p className="text-xs text-gray-500 mb-2">{match.competition}</p>
            <div className="flex items-center justify-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-xs font-bold">
                  {match.homeTeam.substring(0, 2)}
                </div>
                <span className="font-bold text-sm">{match.homeTeam}</span>
              </div>
              
              <div className="flex items-center gap-2 px-3 py-1 bg-white rounded shadow-sm">
                {match.status === 'upcoming' ? (
                  <span className="text-sm font-medium text-gray-600">{match.time}</span>
                ) : (
                  <>
                    <span className="text-lg font-bold">{match.homeScore}</span>
                    <span className="text-gray-400">x</span>
                    <span className="text-lg font-bold">{match.awayScore}</span>
                  </>
                )}
              </div>

              <div className="flex items-center gap-2">
                <span className="font-bold text-sm">{match.awayTeam}</span>
                <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-xs font-bold">
                  {match.awayTeam.substring(0, 2)}
                </div>
              </div>
            </div>
            {match.status === 'live' && (
              <div className="mt-2 text-center">
                <span className="inline-flex items-center gap-1 text-xs font-semibold text-red-600">
                  <span className="w-2 h-2 bg-red-600 rounded-full animate-pulse"></span>
                  AO VIVO
                </span>
              </div>
            )}
          </div>
        ))}
      </div>

      <a 
        href="#"
        className="block mt-3 text-sm text-green-600 font-semibold hover:underline"
      >
        Mais jogos →
      </a>
    </div>
  );
}
