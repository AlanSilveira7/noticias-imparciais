#!/usr/bin/env python3
"""
Script para identificar e excluir imagens abaixo do padrão HD 720p (1280px de largura)
"""

import os
import subprocess
from pathlib import Path

ACERVO_DIR = Path(__file__).parent.parent / 'acervo_temas'
MIN_WIDTH = 1280

def get_image_dimensions(filepath):
    """Obtém dimensões da imagem usando identify do ImageMagick."""
    try:
        result = subprocess.run(
            ['identify', '-format', '%wx%h', str(filepath)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            dims = result.stdout.strip()
            if 'x' in dims:
                w, h = dims.split('x')
                return int(w), int(h)
    except Exception as e:
        print(f"Erro ao obter dimensões de {filepath}: {e}")
    return None, None

def listar_imagens_inadequadas():
    """Lista todas as imagens com largura abaixo de MIN_WIDTH."""
    inadequadas = []
    adequadas = []
    
    for root, dirs, files in os.walk(ACERVO_DIR):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                filepath = Path(root) / file
                w, h = get_image_dimensions(filepath)
                
                if w is not None:
                    rel_path = filepath.relative_to(ACERVO_DIR)
                    if w < MIN_WIDTH:
                        inadequadas.append({
                            'path': filepath,
                            'rel_path': str(rel_path),
                            'width': w,
                            'height': h
                        })
                    else:
                        adequadas.append({
                            'path': filepath,
                            'rel_path': str(rel_path),
                            'width': w,
                            'height': h
                        })
    
    return inadequadas, adequadas

def excluir_imagens(imagens):
    """Exclui as imagens da lista."""
    excluidas = []
    for img in imagens:
        try:
            os.remove(img['path'])
            excluidas.append(img['rel_path'])
            print(f"✗ Excluída: {img['rel_path']} ({img['width']}x{img['height']})")
        except Exception as e:
            print(f"Erro ao excluir {img['rel_path']}: {e}")
    return excluidas

if __name__ == '__main__':
    print("=" * 70)
    print("🧹 LIMPEZA DO ACERVO - IMAGENS ABAIXO DE HD 720p")
    print(f"   Resolução mínima: {MIN_WIDTH}px de largura")
    print("=" * 70)
    
    inadequadas, adequadas = listar_imagens_inadequadas()
    
    print(f"\n📊 RESUMO:")
    print(f"   Total de imagens: {len(inadequadas) + len(adequadas)}")
    print(f"   ✅ Adequadas (>= {MIN_WIDTH}px): {len(adequadas)}")
    print(f"   ⚠️ Inadequadas (< {MIN_WIDTH}px): {len(inadequadas)}")
    
    if inadequadas:
        print(f"\n📋 IMAGENS A SEREM EXCLUÍDAS:")
        for img in inadequadas:
            print(f"   • {img['rel_path']} ({img['width']}x{img['height']})")
        
        print(f"\n🗑️ EXCLUINDO {len(inadequadas)} IMAGENS...")
        excluidas = excluir_imagens(inadequadas)
        print(f"\n✅ {len(excluidas)} imagens excluídas com sucesso!")
    else:
        print("\n✅ Nenhuma imagem inadequada encontrada!")
