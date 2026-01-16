// Formatação automática de valores monetários
document.addEventListener('DOMContentLoaded', function() {
    const amountInputs = document.querySelectorAll('input[name="amount"]');
    
    amountInputs.forEach(input => {
        // Formatação ao digitar
        input.addEventListener('input', function(e) {
            let value = e.target.value;
            
            // Remove tudo que não é número
            value = value.replace(/[^\d]/g, '');
            
            if (value) {
                // Converte para número e divide por 100 para ter centavos
                const numberValue = parseFloat(value) / 100;
                
                // Formata com 2 casas decimais
                const formattedValue = numberValue.toFixed(2);
                
                // Atualiza o valor do input (sem formatação visual, só o valor)
                e.target.value = formattedValue;
            }
        });
        
        // Formatação ao sair do campo
        input.addEventListener('blur', function(e) {
            let value = e.target.value;
            
            if (value) {
                // Garante que tem 2 casas decimais
                const numberValue = parseFloat(value);
                if (!isNaN(numberValue)) {
                    e.target.value = numberValue.toFixed(2);
                }
            }
        });
        
        // Formatação ao entrar no campo
        input.addEventListener('focus', function(e) {
            let value = e.target.value;
            if (value) {
                // Remove formatação para facilitar edição
                e.target.value = value;
            }
        });
    });
});

