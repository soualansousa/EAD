$(document).ready(function() {
    // Enviar o formulário de criação de curso via AJAX
    $('#formCriarCurso').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: "{% url 'cead:criar_curso' %}",
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    alert("Curso criado com sucesso!");
                    location.reload();
                } else {
                    alert("Erro ao criar curso: " + JSON.stringify(response.errors));
                }
            }
        });
    });
    
    $('.button_icon').on('click', function() {
        let cursoId = $(this).data('id'); // Corrigido let para declarar a variável
    
        if (cursoId) {
            $.ajax({
                type: 'GET',
                url: `/detalhar_curso/${cursoId}/`,
                success: function(response) {
                    // Exibindo informações do curso
                    $('#detalheNome').text(response.curso.nome || "Nome não disponível");
                    $('#detalheDescricao').text(response.curso.sobre || "Descrição não disponível");
    
                    // Exibindo as notícias relacionadas ao curso
                    let noticiasHTML = '';
                    if (response.noticias.length > 0) {
                        response.noticias.forEach(function(noticia) {
                            noticiasHTML += `
                                <tr class="text-center table_body" data-id="${noticia.id}">
                                    <td>${noticia.titulo}</td>
                                    <td>${noticia.descricao}</td>
                                    <td>${noticia.publicacao}</td>
                                    <td>${noticia.edicao}</td>
                                </tr>
                            `;
                        });
                        $('#tabelaNoticias tbody').html(noticiasHTML); // Supondo que a tabela tenha um ID "tabelaNoticias"
                    } else {
                        $('#tabelaNoticias tbody').html('<tr><td colspan="5">Nenhuma notícia encontrada.</td></tr>');
                    }
    
                    $('#menuLateral').addClass('open'); // Abre o menu lateral
                },
                error: function() {
                    alert("Erro ao carregar detalhes do curso.");
                }
            });
        } else {
            alert("Erro: ID do curso não encontrado.");
        }
    });

    // Botão para fechar o menu lateral
    $('.button_close').on('click', function() {
        $('#menuLateral').removeClass('open'); // Fecha o menu lateral
    });
});