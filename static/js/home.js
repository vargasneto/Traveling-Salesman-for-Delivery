const escolha = document.getElementById('escolha');
const form = document.getElementById('form');

form.addEventListener('submit', (e) => {
    const min = document.getElementById('cMin').valueAsNumber;
    const max = document.getElementById('cMax').valueAsNumber;

    if (min > max) {
        alert('Erro: O custo mínimo não pode ser maior que o custo máximo.');
        e.preventDefault(); 
    }
});

