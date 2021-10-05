
function relogio(horario){

    let [hora, minuto,segundo] = horario.split(':');
    const ele = document.querySelector('#hora');

    ele.innerHTML = `${hora}:${minuto}:${segundo}`

    hora = parseInt(hora)
    minuto = parseInt(minuto)
    segundo = parseInt(segundo)

    setInterval(()=>{


        if(segundo < 59){

            segundo ++;

        }else{

            segundo = 0;
            
            if(minuto < 59){

                minuto ++;
            }else{

                minuto = 0;

                hora++;
            }
        }

        ele.innerHTML = `${hora < 10 ? '0'+hora : hora}:${minuto <10 ? '0'+minuto: minuto}:${segundo < 10 ? '0'+segundo: segundo}`;
    }, 1000)
  

}


function selecao_filtro(){

    const ele = document.getElementById('selecao-filter')
    const entrada = document.getElementById('campo-busca')

    ele.addEventListener('change',()=>{
                
                let opcao = ele.options[ele.selectedIndex].value

                if( opcao === 'entrada' || opcao === 'saida'){

                    entrada.type='time'

                }else {

                    entrada.type='text'
                }

               
                console.log(opcao)
            }
    )
  

    
}

selecao_filtro()

