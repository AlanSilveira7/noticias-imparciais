"""
Seletor de Imagens V4.2 - Baseado em TEMA (não pessoa)
======================================================
Prioridade: PESSOA COMO SUJEITO/IMPACTADO > TEMA ESPECÍFICO > TEMA GENÉRICO

Este sistema analisa o título da notícia e identifica o TEMA principal,
depois seleciona uma imagem apropriada do acervo curado.

REGRAS:
1. Se a pessoa É o SUJEITO/IMPACTADO da notícia, usar foto da pessoa
   - Ex: "Heleno inicia prisão" → Heleno é impactado → foto do Heleno
   - Ex: "Bolsonaro cancela entrevista" → Bolsonaro é sujeito → foto do Bolsonaro
   - Ex: "Ramagem é alvo de extradição" → Ramagem é impactado → foto do Ramagem
2. Se a pessoa apenas REALIZA uma ação institucional, usar foto do tema
   - Ex: "Moraes concede prisão" → Moraes realiza ação → foto do STF
   - Ex: "Lula sanciona reajuste" → Lula realiza ação → foto do tema (Judiciário)
3. Evitar imagens com marca d'água
"""

import os
import re
import random
from pathlib import Path

# Diretório base do acervo
ACERVO_BASE = "/home/ubuntu/noticias-imparciais/acervo_temas"

# Mapeamento de PESSOAS que podem ser tema principal
PESSOAS_COMO_TEMA = {
    "general_heleno": {
        "nomes": ["general heleno", "augusto heleno", "heleno"],
        "diretorio": "pessoas",
        "filtro": "general_heleno",
        "descricao": "General Augusto Heleno"
    },
    "bolsonaro": {
        "nomes": ["jair bolsonaro", "bolsonaro"],
        "excluir": ["eduardo bolsonaro", "flávio bolsonaro", "carlos bolsonaro"],  # Não confundir com filhos
        "diretorio": "pessoas",
        "filtro": "bolsonaro",
        "descricao": "Jair Bolsonaro"
    },
    "eduardo_bolsonaro": {
        "nomes": ["eduardo bolsonaro"],
        "diretorio": "pessoas",
        "filtro": "eduardo_bolsonaro",
        "descricao": "Eduardo Bolsonaro"
    },
    "ramagem": {
        "nomes": ["ramagem", "alexandre ramagem"],
        "diretorio": "pessoas",
        "filtro": "ramagem",
        "descricao": "Alexandre Ramagem"
    },
    "lula": {
        "nomes": ["lula", "presidente lula"],
        "diretorio": "pessoas",
        "filtro": "lula",
        "descricao": "Presidente Lula"
    }
}

# Palavras que indicam que a pessoa É o SUJEITO/IMPACTADO (usar foto da pessoa)
PESSOA_E_SUJEITO_SE = [
    # Pessoa é impactada/alvo
    "inicia", "cumpre", "cumprimento", "prisão domiciliar", "preso", "presa",
    "detido", "detida", "indiciado", "indiciada", "cassação", "cassado", "cassada",
    "condenado", "condenada", "investigado", "investigada", "depoimento", "depõe",
    "intimado", "intimada", "alvo", "extradição", "extraditado", "deportado",
    "perder passaporte", "perde passaporte", "afastado", "afastada", "suspenso",
    # Pessoa é o sujeito principal da ação (não institucional)
    "cancela", "cancelou", "tem cirurgia", "cirurgia agendada", "internado", "internada",
    "hospitalizado", "hospitalizada", "doente", "saúde", "estado de saúde",
    "viaja", "viajou", "retorna", "retornou", "assume", "assumiu", "renuncia",
    "renunciou", "morre", "morreu", "falece", "faleceu"
]

# Palavras que indicam que a pessoa NÃO é o sujeito (apenas realiza ação institucional)
PESSOA_NAO_E_SUJEITO_SE = [
    "sanciona", "sancionou", "veta", "vetou", "assina", "assinou", 
    "decreta", "decretou", "anuncia", "anunciou", "decide", "decidiu",
    "aprova", "aprovou", "autoriza", "autorizou", "libera", "liberou", 
    "prorroga", "prorrogou", "estende", "estendeu", "concede", "concedeu",
    "determina", "determinou", "ordena", "ordenou", "julga", "julgou",
    "condena", "condenou", "absolve", "absolveu", "arquiva", "arquivou"
]

# Mapeamento de palavras-chave para TEMAS
MAPA_TEMAS = {
    "judiciario": {
        "palavras": [
            "stf", "supremo", "ministro", "ministros", "tribunal", "justiça",
            "judiciário", "juiz", "juízes", "decisão judicial", "julgamento",
            "aposentadoria", "servidor", "servidores", "magistrado", "toga",
            "moraes", "toffoli", "barroso", "fux", "mendes", "lewandowski",
            "nunes marques", "andré mendonça", "dino", "zanin", "weber"
        ],
        "diretorio": "judiciario",
        "descricao": "Decisões judiciais, STF, ministros, servidores do judiciário"
    },
    "legislativo": {
        "palavras": [
            "congresso", "câmara", "senado", "deputado", "deputados", "senador",
            "senadores", "votação", "aprovação", "orçamento", "emenda", "pec",
            "projeto de lei", "pl", "plenário", "lira", "pacheco", "parlamentar",
            "parlamentares", "legislativo", "casa legislativa"
        ],
        "diretorio": "legislativo",
        "descricao": "Votações, aprovações, Congresso, Câmara, Senado"
    },
    "executivo": {
        "palavras": [
            "planalto", "presidente", "governo", "ministério", "ministro",
            "sanção", "sanciona", "veto", "veta", "decreto", "medida provisória",
            "mp", "reunião ministerial", "gabinete"
        ],
        "diretorio": "executivo",
        "descricao": "Ações do governo federal, sanções, decretos"
    },
    "economia": {
        "palavras": [
            "dólar", "real", "moeda", "câmbio", "inflação", "juros", "selic",
            "banco central", "bacen", "b3", "bolsa", "ibovespa", "mercado",
            "economia", "econômico", "pib", "fgts", "previdência", "fiscal",
            "orçamento", "déficit", "superávit", "dívida"
        ],
        "diretorio": "economia",
        "descricao": "Economia, mercado financeiro, Banco Central"
    },
    "eleicoes": {
        "palavras": [
            "eleição", "eleições", "eleitoral", "candidato", "candidatura",
            "urna", "voto", "votação", "tse", "campanha eleitoral", "2026",
            "disputa", "pleito", "segundo turno", "primeiro turno"
        ],
        "diretorio": "eleicoes",
        "descricao": "Eleições, candidaturas, TSE, urnas"
    },
    "seguranca": {
        "palavras": [
            "polícia", "pf", "federal", "operação", "prisão", "preso",
            "criminoso", "crime", "investigação", "inquérito", "mandado",
            "busca", "apreensão", "extradição", "procurado", "foragido",
            "militar", "forças armadas", "passaporte"
        ],
        "diretorio": "seguranca",
        "descricao": "Polícia Federal, operações, prisões, segurança"
    },
    "rodoanel": {
        "palavras": [
            "rodoanel", "rodovia", "trecho norte", "mário covas", "sp-21"
        ],
        "diretorio": "estados",
        "filtro": "rodoanel",
        "descricao": "Rodoanel Mário Covas em São Paulo"
    },
    "rio_janeiro": {
        "palavras": [
            "rio de janeiro", "alerj", "fluminense", "carioca", "guanabara",
            "regime de recuperação fiscal", "estado do rio"
        ],
        "diretorio": "estados",
        "filtro": "alerj_fachada_limpa",
        "descricao": "Estado do Rio de Janeiro, ALERJ"
    },
    "havaianas": {
        "palavras": [
            "havaianas", "alpargatas", "chinelo", "sandália"
        ],
        "diretorio": "marcas",
        "filtro": "havaianas",
        "descricao": "Marca Havaianas"
    }
}


def _normalizar(texto):
    """Normaliza texto para comparação."""
    texto = texto.lower()
    texto = re.sub(r'[áàâã]', 'a', texto)
    texto = re.sub(r'[éèê]', 'e', texto)
    texto = re.sub(r'[íìî]', 'i', texto)
    texto = re.sub(r'[óòôõ]', 'o', texto)
    texto = re.sub(r'[úùû]', 'u', texto)
    texto = re.sub(r'[ç]', 'c', texto)
    return texto


def _contar_matches(titulo_norm, palavras):
    """Conta quantas palavras-chave aparecem no título."""
    count = 0
    for palavra in palavras:
        palavra_norm = _normalizar(palavra)
        if palavra_norm in titulo_norm:
            count += 1
    return count


def _verificar_pessoa_como_sujeito(titulo_norm, titulo_original):
    """
    Verifica se alguma pessoa é o SUJEITO/IMPACTADO da notícia.
    
    Retorna: (pessoa_id, config) ou (None, None)
    """
    # Verificar se alguma pessoa conhecida está no título
    for pessoa_id, config in PESSOAS_COMO_TEMA.items():
        # Verificar exclusões primeiro (ex: não confundir Bolsonaro com Eduardo Bolsonaro)
        if "excluir" in config:
            excluido = False
            for excluir in config["excluir"]:
                if _normalizar(excluir) in titulo_norm:
                    excluido = True
                    break
            if excluido:
                continue
        
        # Verificar se o nome da pessoa está no título
        for nome in config["nomes"]:
            nome_norm = _normalizar(nome)
            if nome_norm in titulo_norm:
                # Verificar se a pessoa É o sujeito/impactado
                pessoa_e_sujeito = any(_normalizar(p) in titulo_norm for p in PESSOA_E_SUJEITO_SE)
                pessoa_nao_e_sujeito = any(_normalizar(p) in titulo_norm for p in PESSOA_NAO_E_SUJEITO_SE)
                
                # Se tem indicadores de que a pessoa É o sujeito e não tem indicadores contrários
                if pessoa_e_sujeito and not pessoa_nao_e_sujeito:
                    return pessoa_id, config
                
                # Caso especial: se a pessoa é mencionada no início do título, provavelmente é o sujeito
                # Ex: "Bolsonaro cancela entrevista" - Bolsonaro é o sujeito
                titulo_lower = titulo_original.lower()
                for nome in config["nomes"]:
                    if titulo_lower.startswith(nome.lower()):
                        # Verificar se não é ação institucional
                        if not pessoa_nao_e_sujeito:
                            return pessoa_id, config
    
    return None, None


def identificar_tema(titulo):
    """
    Identifica o TEMA principal da notícia.
    
    Retorna: (tema_id, score, descricao, config)
    """
    titulo_norm = _normalizar(titulo)
    
    # PASSO 1: Verificar se uma PESSOA é o sujeito/impactado
    pessoa_id, pessoa_config = _verificar_pessoa_como_sujeito(titulo_norm, titulo)
    if pessoa_id:
        return pessoa_id, 100, pessoa_config["descricao"], pessoa_config
    
    # PASSO 2: Verificar temas específicos (maior prioridade)
    temas_especificos = ["rodoanel", "rio_janeiro", "havaianas"]
    for tema_id in temas_especificos:
        config = MAPA_TEMAS[tema_id]
        if any(_normalizar(p) in titulo_norm for p in config["palavras"]):
            return tema_id, 100, config["descricao"], config
    
    # PASSO 3: Calcular score para cada tema genérico
    scores = {}
    for tema_id, config in MAPA_TEMAS.items():
        if tema_id in temas_especificos:
            continue
        score = _contar_matches(titulo_norm, config["palavras"])
        if score > 0:
            scores[tema_id] = score
    
    if not scores:
        config = MAPA_TEMAS["executivo"]
        return "executivo", 0, "Fallback para executivo", config
    
    # Aplicar regras de priorização
    # Regra 1: Se menciona "judiciário", "servidores do judiciário", priorizar judiciário
    if "judiciario" in scores and any(p in titulo_norm for p in ["judiciario", "servidores"]):
        if "executivo" in scores:
            scores["judiciario"] += 2
    
    # Regra 2: Se menciona "orçamento" + "congresso/câmara", priorizar legislativo
    if "legislativo" in scores and "orcamento" in titulo_norm:
        scores["legislativo"] += 2
    
    # Regra 3: Se menciona "eleição" ou "2026" + candidatos, priorizar eleições
    if "eleicoes" in scores and ("2026" in titulo_norm or "eleitoral" in titulo_norm):
        scores["eleicoes"] += 2
    
    # Retornar tema com maior score
    tema_vencedor = max(scores, key=scores.get)
    config = MAPA_TEMAS[tema_vencedor]
    return tema_vencedor, scores[tema_vencedor], config["descricao"], config


def selecionar_imagem(titulo, imagens_usadas=None):
    """
    Seleciona uma imagem do acervo baseada no TEMA da notícia.
    
    Args:
        titulo: Título da notícia
        imagens_usadas: Lista de imagens já usadas (para evitar repetição)
    
    Returns:
        dict com {
            "tema": tema identificado,
            "imagem": caminho da imagem,
            "descricao": descrição do tema
        }
    """
    if imagens_usadas is None:
        imagens_usadas = []
    
    # Identificar tema
    tema_id, score, descricao, config = identificar_tema(titulo)
    
    # Buscar imagens do diretório
    diretorio = os.path.join(ACERVO_BASE, config["diretorio"])
    
    if not os.path.exists(diretorio):
        return {
            "tema": tema_id,
            "imagem": None,
            "descricao": f"Diretório não encontrado: {diretorio}",
            "score": score
        }
    
    # Listar imagens
    imagens = []
    for f in os.listdir(diretorio):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            # Aplicar filtro se existir
            if "filtro" in config:
                if config["filtro"] not in f.lower():
                    continue
            imagens.append(os.path.join(diretorio, f))
    
    if not imagens:
        return {
            "tema": tema_id,
            "imagem": None,
            "descricao": f"Nenhuma imagem encontrada para {tema_id}",
            "score": score
        }
    
    # Filtrar imagens já usadas
    imagens_disponiveis = [img for img in imagens if img not in imagens_usadas]
    
    # Se todas já foram usadas, resetar
    if not imagens_disponiveis:
        imagens_disponiveis = imagens
    
    # Selecionar aleatoriamente
    imagem_selecionada = random.choice(imagens_disponiveis)
    
    return {
        "tema": tema_id,
        "imagem": imagem_selecionada,
        "descricao": descricao,
        "score": score
    }


# Testes
if __name__ == "__main__":
    testes = [
        # Casos onde a PESSOA é o sujeito/impactado
        "General Heleno inicia cumprimento de prisão domiciliar",
        "Bolsonaro cancela entrevista e tem cirurgia agendada para o Natal",
        "Eduardo Bolsonaro pode perder passaporte após cassação de mandato",
        "Ministério da Justiça avança em processo de extradição de Alexandre Ramagem",
        "Alexandre de Moraes concede prisão domiciliar a General Augusto Heleno",
        
        # Casos onde a pessoa apenas REALIZA ação (não é o tema)
        "Lula sanciona reajuste para servidores do Judiciário e veta aumentos futuros",
        "Alexandre de Moraes prorroga permanência do Rio de Janeiro no Regime de Recuperação Fiscal",
        "Toffoli decide sobre aposentadoria integral em casos de doença grave",
        
        # Casos de temas específicos
        "STF decide sobre aposentadoria integral em casos de doença grave não ocupacional",
        "Congresso Nacional aprova Orçamento da União para o próximo exercício",
        "Dólar se mantém acima de R$ 5,50 e Bolsa de Valores registra fechamento em alta",
        "Cenário Eleitoral 2026: Discussões sobre as candidaturas de Zema e Flávio Bolsonaro",
        "Ministro do STF prorroga permanência do Rio de Janeiro no Regime de Recuperação Fiscal",
        "Campanha Publicitária da Havaianas Gera Debate nas Redes Sociais",
        "Inauguração do Trecho Norte do Rodoanel Mário Covas é Marcada por Declarações Políticas",
        "Ministério da Justiça divulga lista de criminosos mais procurados por estado",
    ]
    
    print("=" * 80)
    print("TESTE DO SELETOR DE TEMAS V4.2")
    print("=" * 80)
    
    imagens_usadas = []
    for titulo in testes:
        resultado = selecionar_imagem(titulo, imagens_usadas)
        if resultado["imagem"]:
            imagens_usadas.append(resultado["imagem"])
        
        print(f"\n📰 {titulo[:70]}...")
        print(f"   🏷️  TEMA: {resultado['tema']} (score: {resultado['score']})")
        print(f"   📝 {resultado['descricao']}")
        if resultado["imagem"]:
            print(f"   🖼️  {os.path.basename(resultado['imagem'])}")
        else:
            print(f"   ⚠️  Sem imagem disponível")
