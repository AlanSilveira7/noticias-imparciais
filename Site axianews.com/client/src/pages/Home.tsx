/*
 * HOME PAGE - Clone Globo.com
 * Design: Fidelidade Editorial Clássica
 * 
 * Estrutura:
 * 1. Header com navegação
 * 2. Hero Section (Mobile: texto + card com foto / Desktop: grid de notícias)
 * 3. Três colunas temáticas (Jornalismo, Esporte, Entretenimento)
 * 4. Seção TV Globo
 * 5. Seção Receitas
 * 6. Footer
 */

import Header from '@/components/Header';
import Footer from '@/components/Footer';
import NewsCard from '@/components/NewsCard';
import SectionColumn from '@/components/SectionColumn';


import MobileHeroSection from '@/components/MobileHeroSection';

// Mock data for news
const heroNews = {
  title: 'Caso Master: Vorcaro conclui depoimento; PF ainda avalia acareação',
  image: '/images/hero-news-1.jpg',
  category: 'ECONOMIA',
  subtitle: 'Empresário prestou esclarecimentos sobre operações financeiras',
  bullets: [
    'Blog: perguntas de Toffoli pedem que Vorcaro avalie atuação do BC',
    'Valdo Cruz: Banco Central cita nova apuração sobre fraudes',
  ],
};

// Mobile hero data
const mobileMainNews = {
  title: 'Correios recebem R$ 10 bilhões em empréstimos após acordo com bancos',
  bullets: [
    'TST resolve impasse entre Correios e funcionários: reajuste anual de 5,1%',
    'Em crise, Correios registram leve alta de receitas com encomendas',
  ],
};

const mobilePhotoNews = {
  title: 'Portugal suspende novo sistema de imigração após caos',
  image: 'https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=600&h=450&fit=crop',
  bullet: 'Aeroporto registrou filas de até 9 horas em Lisboa',
};

const featuredNews = [
  {
    title: 'Com salário de R$ 400 mil, Lucas Lima recusa oferta de reajuste do Sport',
    image: '/images/sports-soccer.jpg',
    source: 'ge',
    sourceColor: '#00A859',
    bullets: ['River Plate faz consulta por Viña, do Flamengo; veja condições'],
  },
  {
    title: 'Shawn Mendes e Bruna Marquezine são clicados aos beijos; veja vídeo',
    image: '/images/entertainment-celebrity.jpg',
    source: 'Quem',
    sourceColor: '#E91E63',
    bullets: ['Veja a casa onde os dois vão passar o Réveillon juntos'],
  },
];

const sideNews = [
  {
    title: 'Portugal suspende novo sistema de imigração após caos',
    image: 'https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=200&h=150&fit=crop',
    source: 'g1',
  },
  {
    title: 'Virada de ano deve ter chuva forte pelo país; veja a previsão',
    image: '/images/news-weather.jpg',
    source: 'g1',
  },
  {
    title: 'Ressaca no Rio prevê ondas de até 2,5 m durante o réveillon',
    image: 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=200&h=150&fit=crop',
    source: 'g1',
  },
];

const journalismNews = [
  {
    title: 'Virada de ano deve ter chuva forte pelo país; veja a previsão',
    image: 'https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=400&h=300&fit=crop',
    category: 'Clima',
    source: 'g1',
    bullet: 'Mega-Sena: quanto rende R$ 1 bilhão na poupança?',
  },
  {
    title: 'Ressaca no Rio prevê ondas de até 2,5 m durante o réveillon',
    image: 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400&h=300&fit=crop',
    category: 'Rio de Janeiro',
    source: 'g1',
    bullet: 'RJ: Paes celebra recorde do réveillon no Guinness',
  },
  {
    title: 'Trens colidem a caminho de Machu Picchu; há feridos',
    image: 'https://images.unsplash.com/photo-1526392060635-9d6019884377?w=400&h=300&fit=crop',
    category: 'Mundo',
    source: 'g1',
    bullet: '2025 foi um dos três anos mais quentes registrados',
  },
  {
    title: 'Bolsa tem melhor desempenho em 9 anos ao subir 33,95%',
    image: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&h=300&fit=crop',
    category: 'Economia',
    source: 'Valor',
    bullet: 'Dólar cai e tem maior queda em quase 10 anos',
  },
  {
    title: 'Após 27 anos, homem que cruzou a Terra a pé está prestes a chegar em casa',
    image: 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=400&h=300&fit=crop',
    category: 'Mundo',
    source: 'O Globo',
    bullet: 'Motorista é preso viajando em ônibus batido, sem para-brisa',
  },
];

const sportsNews = [
  {
    title: 'Com salário de R$ 400 mil, Lucas Lima recusa oferta de reajuste do Sport',
    image: 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400&h=300&fit=crop',
    category: 'Futebol',
    source: 'ge',
    bullet: 'River Plate faz consulta por Viña, do Flamengo; veja condições',
  },
  {
    title: 'FBI apreende coleção de motos de R$ 223 mi ligada a ex-atleta olímpico',
    image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
    category: 'Olimpíadas',
    source: 'ge',
    bullet: 'Atleta brasileiro é banido por doping em competição internacional',
  },
  {
    title: 'Sobe e desce da F1: veja quem foi bem e quem foi mal em 2025',
    image: 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=400&h=300&fit=crop',
    category: 'Fórmula 1',
    source: 'ge',
    bullet: 'Hamilton revela bastidores da mudança para Ferrari',
  },
  {
    title: 'Grêmio 2025: vote na melhor e na pior contratação do clube',
    image: 'https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400&h=300&fit=crop',
    category: 'Gaúcho',
    source: 'ge',
    bullet: 'O que credencia cinco jovens do Grêmio a serem chamados para o Gauchão',
  },
  {
    title: 'Filho de Zidane decide não jogar pela França e atua por rival histórico',
    image: 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=400&h=300&fit=crop',
    category: 'Internacional',
    source: 'ge',
    bullet: 'Mbappé sofre lesão e desfalca Real Madrid por três semanas',
  },
];

const entertainmentNews = [
  {
    title: 'Shawn Mendes e Bruna Marquezine são clicados aos beijos; veja vídeo',
    image: 'https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=400&h=300&fit=crop',
    category: 'Celebridades',
    source: 'Quem',
    bullet: 'Veja a casa onde os dois vão passar o Réveillon juntos',
  },
  {
    title: 'Alessandra Ambrosio e namorado gringo beijam muito em Fernando de Noronha',
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
    category: 'Famosos na Praia',
    source: 'Quem',
    bullet: 'Modelo exibe corpão em cliques de biquíni na praia',
  },
  {
    title: 'Rafaella Santos, irmã de Neymar, posta foto de jantar romântico com Gabigol',
    image: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400&h=300&fit=crop',
    category: 'Amor e Sexo',
    source: 'Quem',
    bullet: 'Casal é visto em clima de romance durante viagem',
  },
  {
    title: "Ex-BBB Amanda Meirelles fala sobre transformação do seu rosto: 'Sempre criticando'",
    image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=300&fit=crop',
    category: 'Estética',
    source: 'Quem',
    bullet: 'Influenciadora revela procedimentos estéticos que já fez',
  },
  {
    title: "Giovanna Ewbank abre álbum de férias em destino paradisíaco na Bahia",
    image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=300&fit=crop',
    category: 'Celebridades',
    source: 'Marie Claire',
    bullet: 'Atriz compartilha momentos em família nas redes sociais',
  },
];

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      
      <main className="flex-1">
        {/* Mobile Hero Section - Only visible on mobile/tablet */}
        <MobileHeroSection
          mainNews={mobileMainNews}
          photoNews={mobilePhotoNews}
        />

        {/* Desktop Hero Section - Only visible on desktop */}
        <section className="hidden lg:block bg-white">
          <div className="container py-4">
            <div className="grid grid-cols-12 gap-4">
              {/* Main Hero */}
              <div className="col-span-6">
                <NewsCard
                  title={heroNews.title}
                  image={heroNews.image}
                  category={heroNews.category}
                  subtitle={heroNews.subtitle}
                  bullets={heroNews.bullets}
                  variant="hero"
                />
              </div>

              {/* Featured News */}
              <div className="col-span-3 space-y-4">
                {featuredNews.map((news, index) => (
                  <NewsCard
                    key={index}
                    title={news.title}
                    image={news.image}
                    source={news.source}
                    sourceColor={news.sourceColor}
                    bullets={news.bullets}
                    variant="featured"
                  />
                ))}
              </div>

              {/* Side News */}
              <div className="col-span-3 space-y-3">
                {sideNews.map((news, index) => (
                  <NewsCard
                    key={index}
                    title={news.title}
                    image={news.image}
                    source={news.source}
                    variant="small"
                  />
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Three Columns Section */}
        <section className="py-6">
          <div className="container">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Política Column */}
              <SectionColumn
                title="Política"
                color="#FF0000"
                news={journalismNews}
              />

              {/* Economia Column */}
              <SectionColumn
                title="Economia"
                color="#FF6B00"
                news={entertainmentNews}
              />

              {/* Tecnologia Column */}
              <SectionColumn
                title="Tecnologia"
                color="#00A859"
                news={sportsNews}
              />
            </div>
          </div>
        </section>


      </main>

      <Footer />
    </div>
  );
}
