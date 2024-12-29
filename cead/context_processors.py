from django.urls import resolve

def breadcrumbs(request):
    path = request.path.strip("/").split("/")
    breadcrumbs = [{"name": "Início", "url": "/"}]
    url_accum = ""

    for part in path:
        # Ignore "cead" ou "coo" no caminho
        if part in ["cead", "coo"]:
            continue

        url_accum += f"/{part}"
        breadcrumbs.append({"name": part.capitalize(), "url": url_accum})

    return {"breadcrumbs": breadcrumbs}


