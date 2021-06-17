$(document).ready(function () {


    //Apresentação de telas-----------------------------//
    $(`#home`).click(function () {
        $(`#Clients_view`).hide()
        $(`#Command_view`).hide()
        $(`#Home_view`).show()
    })

    $(`#clientes`).click(function () {
        $(`#Clients_view`).show()
        $(`#Command_view`).hide()
        $(`#Home_view`).hide()
    })

    $(`#comandos`).click(function () {
        $(`#Clients_view`).hide()
        $(`#Home_view`).hide()
        $(`#Command_view`).show()
    })
    //Apresentação de telas-----------------------------//

    //Função para inicializar o servidor
    $(`#start_server`).click(function () {
        eel.init_server()(function (data) {
            if (data) {
                $(`#start_server`).prop('disabled', true);
                $(`#status_server`).show()
                console.log(`servidor:${data}`);
            }
            else {
                alert(`Problema ao inicializar o servidor`)
            }
        });
    });

    //Função para exibir os clientes
    $(`#clientes`).click(function () {
        eel.list_connections()(function (data) {
            $(`#cli-list`).empty()
            data.forEach(function (item, index) {
                $(`#cli-list`).append(`<tr class="select_cli" data-cli=${index + 1}>
                <td>Cliente ${index + 1}</td>
                <td><span class="mif-user icon fg-green"> Conectado</span></td>
                
                </tr>`)
                })

        });
    })

    //Função para selecionar cliente
    $(document).on(`click`, `.select_cli`, function () {
        id = $(this).attr("data-cli")
        outher_this = this

        eel.cli_selected(id)(function (data) {
            if (data == true) {
                $(`.select_cli`).find(`span`).removeClass(`mif-target icon fg-red`).addClass("mif-user icon fg-green");
                $(outher_this).find(`span`).removeClass(`mif-user icon fg-green`).addClass("mif-target icon fg-red");
                alert(`cliente #${id} selecionado`)
                $(`#output_command`).html('')
            }
        });
    });



    //Função para enviar os comandos
    $(`#send_command`).click(function () {
        command = $(`#command_input`).val()
        command_show = `[${command}]`
        console.log($(`#output_command`).val() == '');
        if($(`#output_command`).val() == ''){
            $(`#output_command`).html(command_show + '\n')
        }
        else {
            $(`#output_command`).append(command_show + '\n')

        }
        eel.send_command(command)(function (data) {
            $(`#output_command`).append(data)
        });
    })

});


