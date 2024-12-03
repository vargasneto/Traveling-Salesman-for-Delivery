document.getElementById('gerar-problema-btn').addEventListener('click', function() {
    document.getElementById('matriz-container').classList.remove('hidden');
    document.getElementById('solucao-inicial-container').classList.add('hidden');
});

document.getElementById('solucao-inicial-btn').addEventListener('click', function() {
    document.getElementById('solucao-inicial-container').classList.remove('hidden');
    document.getElementById('matriz-container').classList.add('hidden');
});

document.getElementById('avalia-btn').addEventListener('click', function() {
    document.getElementById('avalia-container').classList.remove('hidden');
});