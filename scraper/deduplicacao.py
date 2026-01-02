#!/usr/bin/env python3
"""
Módulo de Deduplicação Inteligente
Projeto: Axia News
Data: 23/12/2025

Este módulo gerencia a deduplicação de notícias, decidindo se uma notícia
deve ser publicada como nova, atualizar uma existente, ou ser linkada
como relacionada.
"""

import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from similaridade import (
    calcular_similaridade,
    classificar_similaridade,
    encontrar_noticias_similares,
    decidir_acao
)


class GerenciadorDeduplicacao:
    """
    Gerencia a deduplicação de notícias com base em similaridade.
    """
    
    def __init__(self, dias_comparacao: int = 2, limiar_duplicata: float = 0.85, limiar_relacionada: float = 0.50):
        """
        Inicializa o gerenciador.
        
        Args:
            dias_comparacao: Quantos dias para trás comparar
            limiar_duplicata: Similaridade mínima para considerar duplicata
            limiar_relacionada: Similaridade mínima para considerar relacionada
        """
        self.dias_comparacao = dias_comparacao
        self.limiar_duplicata = limiar_duplicata
        self.limiar_relacionada = limiar_relacionada
        
        # Estatísticas
        self.stats = {
            'novas': 0,
            'atualizadas': 0,
            'relacionadas': 0,
            'descartadas': 0
        }
    
    def processar_noticias(
        self,
        noticias_novas: List[Dict],
        historico: List[Dict]
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Processa uma lista de notícias novas contra o histórico.
        
        Args:
            noticias_novas: Lista de notícias a serem processadas
            historico: Histórico de notícias existentes
        
        Returns:
            Tupla com:
            - Lista de notícias processadas (novas + atualizadas)
            - Histórico atualizado
        """
        print(f"\n[DEDUPLICAÇÃO] Processando {len(noticias_novas)} notícias...")
        print(f"    Histórico: {len(historico)} notícias")
        print(f"    Período de comparação: últimos {self.dias_comparacao} dias")
        
        noticias_processadas = []
        historico_atualizado = historico.copy()
        
        for noticia in noticias_novas:
            resultado = self._processar_noticia(noticia, historico_atualizado)
            
            if resultado['acao'] == 'publicar_nova':
                # Adiciona campos de relacionamento
                noticia_final = self._preparar_noticia_nova(noticia, resultado['relacionadas'])
                noticias_processadas.append(noticia_final)
                self.stats['novas'] += 1
                
            elif resultado['acao'] == 'atualizar_existente':
                # Atualiza a notícia existente no histórico
                noticia_atualizada = self._atualizar_noticia(
                    resultado['noticia_principal'],
                    noticia,
                    resultado['relacionadas']
                )
                # Substitui no histórico
                historico_atualizado = self._substituir_no_historico(
                    historico_atualizado,
                    noticia_atualizada
                )
                noticias_processadas.append(noticia_atualizada)
                self.stats['atualizadas'] += 1
                
            elif resultado['acao'] == 'publicar_relacionada':
                # Publica como nova mas com links para relacionadas
                noticia_final = self._preparar_noticia_nova(noticia, resultado['relacionadas'])
                noticias_processadas.append(noticia_final)
                self.stats['relacionadas'] += 1
        
        self._imprimir_estatisticas()
        
        return noticias_processadas, historico_atualizado
    
    def _processar_noticia(self, noticia: Dict, historico: List[Dict]) -> Dict:
        """
        Processa uma única notícia e decide a ação.
        """
        titulo = noticia.get('title', noticia.get('titulo', ''))
        
        # Encontra similares
        similares = encontrar_noticias_similares(
            noticia,
            historico,
            self.dias_comparacao,
            campo_titulo='title'
        )
        
        if not similares:
            return {
                'acao': 'publicar_nova',
                'noticia_principal': None,
                'relacionadas': []
            }
        
        # Analisa a mais similar
        mais_similar, similaridade, classificacao = similares[0]
        
        # Coleta relacionadas (entre 50% e 85%)
        relacionadas = [
            n for n, sim, cls in similares
            if self.limiar_relacionada <= sim < self.limiar_duplicata
        ]
        
        print(f"    → '{titulo[:50]}...'")
        print(f"      Mais similar: {similaridade:.1%} ({classificacao})")
        
        if similaridade >= self.limiar_duplicata:
            return {
                'acao': 'atualizar_existente',
                'noticia_principal': mais_similar,
                'relacionadas': relacionadas
            }
        elif similaridade >= self.limiar_relacionada:
            return {
                'acao': 'publicar_relacionada',
                'noticia_principal': None,
                'relacionadas': relacionadas
            }
        else:
            return {
                'acao': 'publicar_nova',
                'noticia_principal': None,
                'relacionadas': relacionadas
            }
    
    def _preparar_noticia_nova(self, noticia: Dict, relacionadas: List[Dict]) -> Dict:
        """
        Prepara uma notícia nova com campos adicionais.
        """
        noticia_final = noticia.copy()
        
        # Adiciona campos de controle
        noticia_final['version'] = 1
        noticia_final['createdAt'] = noticia.get('date', datetime.now().strftime('%d/%m/%Y'))
        noticia_final['updatedAt'] = None
        noticia_final['originalId'] = None
        
        # Adiciona IDs das relacionadas
        noticia_final['relatedNews'] = [
            n.get('id', '') for n in relacionadas[:3]  # Máximo 3 relacionadas
        ]
        
        return noticia_final
    
    def _atualizar_noticia(
        self,
        noticia_existente: Dict,
        noticia_nova: Dict,
        relacionadas: List[Dict]
    ) -> Dict:
        """
        Atualiza uma notícia existente com novos dados.
        """
        noticia_atualizada = noticia_existente.copy()
        
        # Incrementa versão
        versao_atual = noticia_existente.get('version', 1)
        noticia_atualizada['version'] = versao_atual + 1
        
        # Atualiza data de modificação
        noticia_atualizada['updatedAt'] = datetime.now().strftime('%d/%m/%Y')
        
        # Preserva data original
        if 'createdAt' not in noticia_atualizada:
            noticia_atualizada['createdAt'] = noticia_existente.get('date', '')
        
        # Atualiza conteúdo se o novo for mais completo
        conteudo_existente = noticia_existente.get('content', '')
        conteudo_novo = noticia_nova.get('content', noticia_nova.get('sintese', ''))
        
        if len(conteudo_novo) > len(conteudo_existente):
            noticia_atualizada['content'] = conteudo_novo
            noticia_atualizada['summary'] = noticia_nova.get('summary', noticia_nova.get('sintese', ''))[:200]
        
        # Atualiza relacionadas
        relacionadas_existentes = set(noticia_existente.get('relatedNews', []))
        novas_relacionadas = {n.get('id', '') for n in relacionadas[:3]}
        noticia_atualizada['relatedNews'] = list(relacionadas_existentes | novas_relacionadas)[:5]
        
        print(f"      ✓ Atualizada para versão {noticia_atualizada['version']}")
        
        return noticia_atualizada
    
    def _substituir_no_historico(self, historico: List[Dict], noticia_atualizada: Dict) -> List[Dict]:
        """
        Substitui uma notícia no histórico pela versão atualizada.
        """
        id_noticia = noticia_atualizada.get('id', '')
        
        for i, n in enumerate(historico):
            if n.get('id', '') == id_noticia:
                historico[i] = noticia_atualizada
                return historico
        
        # Se não encontrou, adiciona
        historico.insert(0, noticia_atualizada)
        return historico
    
    def _imprimir_estatisticas(self):
        """
        Imprime estatísticas do processamento.
        """
        print(f"\n    Estatísticas de deduplicação:")
        print(f"      - Notícias novas: {self.stats['novas']}")
        print(f"      - Notícias atualizadas: {self.stats['atualizadas']}")
        print(f"      - Com relacionadas: {self.stats['relacionadas']}")
    
    def resetar_estatisticas(self):
        """
        Reseta as estatísticas.
        """
        self.stats = {
            'novas': 0,
            'atualizadas': 0,
            'relacionadas': 0,
            'descartadas': 0
        }


def processar_com_deduplicacao(
    noticias_novas: List[Dict],
    historico: List[Dict],
    dias_comparacao: int = 2
) -> Tuple[List[Dict], List[Dict]]:
    """
    Função de conveniência para processar notícias com deduplicação.
    
    Args:
        noticias_novas: Lista de notícias novas
        historico: Histórico existente
        dias_comparacao: Dias para comparação
    
    Returns:
        Tupla (notícias_processadas, histórico_atualizado)
    """
    gerenciador = GerenciadorDeduplicacao(dias_comparacao=dias_comparacao)
    return gerenciador.processar_noticias(noticias_novas, historico)


# Teste
if __name__ == '__main__':
    # Simula histórico
    historico = [
        {
            'id': 'bolsonaro-cirurgia-1',
            'title': 'Bolsonaro cancela entrevista e tem cirurgia agendada',
            'date': '22/12/2025',
            'content': 'Conteúdo original...',
            'category': 'política'
        },
        {
            'id': 'lula-indulto-1',
            'title': 'Lula assina indulto de Natal',
            'date': '22/12/2025',
            'content': 'Conteúdo sobre indulto...',
            'category': 'política'
        }
    ]
    
    # Simula notícias novas
    noticias_novas = [
        {
            'id': 'bolsonaro-cirurgia-2',
            'title': 'Bolsonaro cancela entrevista por motivo de cirurgia no Natal',
            'date': '23/12/2025',
            'content': 'Conteúdo atualizado com mais detalhes sobre a cirurgia...',
            'category': 'política'
        },
        {
            'id': 'dolar-alta-1',
            'title': 'Dólar fecha em alta nesta segunda-feira',
            'date': '23/12/2025',
            'content': 'Conteúdo sobre o dólar...',
            'category': 'economia'
        }
    ]
    
    print("=== Teste de Deduplicação ===\n")
    
    processadas, historico_atualizado = processar_com_deduplicacao(
        noticias_novas,
        historico
    )
    
    print(f"\n=== Resultado ===")
    print(f"Notícias processadas: {len(processadas)}")
    print(f"Histórico atualizado: {len(historico_atualizado)}")
    
    for n in processadas:
        print(f"\n  - {n['title'][:50]}...")
        print(f"    Versão: {n.get('version', 1)}")
        print(f"    Relacionadas: {n.get('relatedNews', [])}")
