import { Link } from "wouter";
import { Scale, Eye, Brain, FileCheck, Target, Shield, Users, Zap, ArrowLeft } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function About() {
  return (
    <div className="min-h-screen bg-white">
      <Header />

      <main>
        {/* Breadcrumb */}
        <div className="border-b border-gray-100">
          <div className="container py-3">
            <nav className="flex items-center gap-2 text-sm text-gray-500">
              <Link href="/" className="hover:text-blue-600">Início</Link>
              <span>/</span>
              <span className="text-gray-900">Sobre</span>
            </nav>
          </div>
        </div>

        {/* Hero */}
        <section className="container py-12">
          <div className="max-w-3xl">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                <Scale className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Sobre o Axia News
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed">
              Em um cenário de crescente polarização política, acreditamos que o acesso 
              a informação equilibrada é fundamental para uma democracia saudável.
            </p>
          </div>
        </section>

        {/* Mission */}
        <section className="bg-gray-50 border-y border-gray-200">
          <div className="container py-12">
            <div className="max-w-3xl">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Nossa Missão
              </h2>
              <div className="space-y-4 text-gray-700 leading-relaxed">
                <p>
                  O Axia News nasceu da necessidade de oferecer uma alternativa 
                  ao jornalismo polarizado que domina o cenário brasileiro. Nossa missão é 
                  fornecer aos leitores uma visão completa e equilibrada dos acontecimentos, 
                  permitindo que formem suas próprias opiniões baseadas em fatos, não em 
                  narrativas enviesadas.
                </p>
                <p>
                  Utilizamos tecnologia de inteligência artificial para analisar como diferentes 
                  veículos de comunicação cobrem os mesmos eventos, identificando vieses 
                  editoriais, linguagem carregada e omissões. A partir dessa análise, geramos 
                  uma versão imparcial que apresenta os fatos objetivos e mostra claramente 
                  como cada lado político aborda a questão.
                </p>
                <p>
                  Não pretendemos dizer ao leitor o que pensar. Nosso papel é apresentar 
                  a informação de forma transparente e deixar que você, leitor, tire suas 
                  próprias conclusões.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Methodology */}
        <section className="container py-12">
          <div className="text-center mb-10">
            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              Como Funciona
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Nossa metodologia combina tecnologia avançada com princípios jornalísticos 
              rigorosos para garantir imparcialidade.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Eye className="w-5 h-5 text-blue-600" />
              </div>
              <h3 className="font-bold text-gray-900 mb-2">1. Monitoramento</h3>
              <p className="text-gray-600 text-sm">
                Acompanhamos diariamente os principais veículos de comunicação brasileiros, 
                incluindo fontes de diferentes orientações políticas.
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Brain className="w-5 h-5 text-blue-600" />
              </div>
              <h3 className="font-bold text-gray-900 mb-2">2. Análise de Viés</h3>
              <p className="text-gray-600 text-sm">
                Nossa IA analisa cada notícia identificando fatos objetivos, linguagem 
                carregada, omissões e diferenças de enquadramento.
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Target className="w-5 h-5 text-blue-600" />
              </div>
              <h3 className="font-bold text-gray-900 mb-2">3. Comparação</h3>
              <p className="text-gray-600 text-sm">
                Comparamos como o mesmo evento é coberto por fontes de esquerda e direita, 
                identificando pontos em comum e divergências.
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <FileCheck className="w-5 h-5 text-green-600" />
              </div>
              <h3 className="font-bold text-gray-900 mb-2">4. Síntese Imparcial</h3>
              <p className="text-gray-600 text-sm">
                Geramos uma versão neutra da notícia, apresentando os fatos e mostrando 
                claramente a perspectiva de cada lado.
              </p>
            </div>
          </div>
        </section>

        {/* Sources */}
        <section className="bg-gray-50 border-y border-gray-200">
          <div className="container py-12">
            <div className="max-w-3xl mx-auto">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Nossas Fontes
              </h2>
              <p className="text-gray-600 mb-8">
                Para garantir uma análise equilibrada, monitoramos veículos de diferentes 
                orientações editoriais. Atualmente, nossas principais fontes incluem:
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white border-l-4 border-red-500 rounded-r-lg p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="w-3 h-3 rounded-full bg-red-500"></span>
                    <h3 className="font-bold text-gray-900">Fontes de Esquerda</h3>
                  </div>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li>• UOL</li>
                    <li>• G1 / Globo</li>
                    <li>• Folha de S. Paulo</li>
                  </ul>
                </div>

                <div className="bg-white border-l-4 border-blue-500 rounded-r-lg p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="w-3 h-3 rounded-full bg-blue-500"></span>
                    <h3 className="font-bold text-gray-900">Fontes de Direita</h3>
                  </div>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li>• Revista Oeste</li>
                    <li>• Brasil Paralelo</li>
                    <li>• Gazeta do Povo</li>
                  </ul>
                </div>
              </div>

              <p className="text-gray-500 text-sm mt-6">
                A classificação das fontes é baseada em análises acadêmicas e observação 
                editorial. Estamos constantemente expandindo nossa cobertura para incluir 
                mais veículos e perspectivas.
              </p>
            </div>
          </div>
        </section>

        {/* Values */}
        <section className="container py-12">
          <div className="text-center mb-10">
            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              Nossos Valores
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="w-7 h-7 text-green-600" />
              </div>
              <h3 className="font-bold text-gray-900 mb-2">Transparência</h3>
              <p className="text-gray-600 text-sm">
                Mostramos claramente nossas fontes, metodologia e como chegamos às 
                nossas conclusões.
              </p>
            </div>

            <div className="text-center">
              <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-7 h-7 text-blue-600" />
              </div>
              <h3 className="font-bold text-gray-900 mb-2">Respeito ao Leitor</h3>
              <p className="text-gray-600 text-sm">
                Não tentamos convencer ou manipular. Apresentamos os fatos e deixamos 
                você decidir.
              </p>
            </div>

            <div className="text-center">
              <div className="w-14 h-14 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="w-7 h-7 text-purple-600" />
              </div>
              <h3 className="font-bold text-gray-900 mb-2">Inovação</h3>
              <p className="text-gray-600 text-sm">
                Usamos tecnologia de ponta para oferecer uma experiência de consumo 
                de notícias mais inteligente.
              </p>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-gray-900 text-white">
          <div className="container py-12 text-center">
            <h2 className="text-2xl font-bold mb-4">
              Junte-se a nós nessa jornada
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto mb-6">
              Acreditamos que informação de qualidade é um direito de todos. 
              Acompanhe nossas notícias e faça parte de uma comunidade que valoriza 
              a verdade acima de narrativas.
            </p>
            <Link 
              href="/" 
              className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Ver Notícias
            </Link>
          </div>
        </section>

        {/* Back link */}
        <section className="container py-8">
          <Link 
            href="/" 
            className="inline-flex items-center gap-2 text-blue-600 hover:underline font-medium"
          >
            <ArrowLeft size={16} />
            Voltar para a página inicial
          </Link>
        </section>
      </main>

      <Footer />
    </div>
  );
}
