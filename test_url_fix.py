#!/usr/bin/env python3
"""
Script de teste para verificar as correções de URL
"""

def clean_and_validate_url(url):
    """
    Limpa e valida uma URL, corrigindo problemas comuns
    
    Args:
        url: URL a ser limpa
        
    Returns:
        str: URL limpa e válida ou None se inválida
    """
    if not url:
        return None
    
    # Remove espaços e caracteres de controle
    url = url.strip()
    
    # Remove quebras de linha e tabs
    url = url.replace('\n', '').replace('\r', '').replace('\t', '')
    
    # Corrige problema comum de URLs duplicadas
    # Ex: "https://www.youtube.cohttps://www.youtube.com/..."
    if 'https://www.youtube.cohttps://' in url:
        # Extrai a URL correta
        start_pos = url.find('https://www.youtube.com/')
        if start_pos > 0:  # Se há uma segunda ocorrência
            url = url[start_pos:]
    
    # Corrige outros problemas similares
    patterns_to_fix = [
        ('http://www.youtube.cohttp://', 'http://'),
        ('https://youtu.behttps://', 'https://'),
        ('http://youtu.behttp://', 'http://'),
    ]
    
    for pattern, replacement in patterns_to_fix:
        if pattern in url:
            start_pos = url.find(replacement, len(pattern) - len(replacement))
            if start_pos > 0:
                url = url[start_pos:]
    
    # Validação básica de formato de URL
    if not (url.startswith('http://') or url.startswith('https://')):
        return None
    
    # Validação específica para plataformas suportadas
    supported_domains = [
        'youtube.com', 'youtu.be', 'm.youtube.com',
        'streamyard.com', 'vimeo.com', 'dailymotion.com',
        'twitch.tv', 'facebook.com', 'instagram.com'
    ]
    
    url_lower = url.lower()
    is_supported = any(domain in url_lower for domain in supported_domains)
    
    if not is_supported:
        # Permite outras URLs, mas avisa
        print(f"Aviso: Domínio pode não ser suportado: {url}")
    
    return url


def test_url_cleaning():
    """Testa a função de limpeza de URLs"""
    
    test_cases = [
        # Caso 1: URL normal (deve permanecer igual)
        {
            'input': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'expected': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'description': 'URL normal do YouTube'
        },
        
        # Caso 2: URL corrompida (como reportado no bug)
        {
            'input': 'https://www.youtube.cohttps://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'expected': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'description': 'URL corrompida com duplicação'
        },
        
        # Caso 3: URL com espaços
        {
            'input': '  https://www.youtube.com/watch?v=dQw4w9WgXcQ  ',
            'expected': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'description': 'URL com espaços'
        },
        
        # Caso 4: URL com quebras de linha
        {
            'input': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ\n',
            'expected': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'description': 'URL com quebra de linha'
        },
        
        # Caso 5: URL inválida
        {
            'input': 'not-a-url',
            'expected': None,
            'description': 'URL inválida'
        },
        
        # Caso 6: YouTube curto
        {
            'input': 'https://youtu.be/dQw4w9WgXcQ',
            'expected': 'https://youtu.be/dQw4w9WgXcQ',
            'description': 'URL curta do YouTube'
        }
    ]
    
    print("🧪 Testando função de limpeza de URLs...\n")
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        result = clean_and_validate_url(test['input'])
        passed = result == test['expected']
        all_passed = all_passed and passed
        
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"Teste {i}: {test['description']}")
        print(f"  Input:    {repr(test['input'])}")
        print(f"  Expected: {repr(test['expected'])}")
        print(f"  Result:   {repr(result)}")
        print(f"  Status:   {status}")
        print()
    
    print("=" * 50)
    if all_passed:
        print("🎉 Todos os testes passaram!")
    else:
        print("⚠️ Alguns testes falharam!")
    
    return all_passed


if __name__ == '__main__':
    test_url_cleaning()