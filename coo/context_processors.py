def breadcrumbs(request):
    """
    Retorna um contexto contendo o caminho atual dividido em breadcrumbs,
    ignorando ou renomeando o segmento inicial 'coo'.
    """
    path = request.path.strip('/').split('/')
    
    # Lista de breadcrumbs começando com "Início"
    breadcrumbs = [{'name': 'Início', 'url': '/'}]

    current_path = ''
    for index, segment in enumerate(path):
        # Pule o segmento inicial "coo"
        if index == 0 and segment == 'coo':
            continue
        current_path += f"{segment}/"
        breadcrumbs.append({'name': segment.title(), 'url': f"/{current_path}"})

    return {'breadcrumbs': breadcrumbs}

