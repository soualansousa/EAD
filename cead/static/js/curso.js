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
    
    // Botão para abrir o menu lateral com detalhes do curso
    $('.button_icon').on('click', function() {
        let cursoId = $(this).data('id'); // Corrigido let para declarar a variável

        if (cursoId) {
            $.ajax({
                type: 'GET',
                url: `/detalhar_curso/${cursoId}/`,
                success: function(response) {
                    $('#detalheNome').text(response.nome || "Nome não disponível");
                    $('#detalheDescricao').text(response.descricao || "Descrição não disponível");    
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