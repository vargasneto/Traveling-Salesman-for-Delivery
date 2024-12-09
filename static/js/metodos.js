document.getElementById('base-btn').addEventListener('click', function() {
    document.getElementById('base-container').classList.remove('hidden');
    document.getElementById('buscaLocal-container').classList.add('hidden');
});

document.getElementById('buscaLocal-btn').addEventListener('click', function() {
    document.getElementById('buscaLocal-container').classList.remove('hidden');
    document.getElementById('base-container').classList.add('hidden');
});

document.getElementById('modalbtn').addEventListener('click', function() {
    document.getElementById('base-container').classList.add('hidden');
    document.getElementById('buscaLocal-container').classList.add('hidden');
});

