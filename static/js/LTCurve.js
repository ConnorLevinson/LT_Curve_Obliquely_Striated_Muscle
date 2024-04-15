document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const loading = document.getElementById('loading');
    const graphContent = document.getElementById('main');


    if (localStorage.getItem('angle')) {
        document.getElementById('angle').value = localStorage.getItem('angle');
        document.getElementById('A').value = localStorage.getItem('A');
        document.getElementById('I').value = localStorage.getItem('I');
        document.getElementById('BZ').value = localStorage.getItem('BZ');

        localStorage.removeItem('angle');
        localStorage.removeItem('A');
        localStorage.removeItem('I');
        localStorage.removeItem('BZ');
    }

    form.onsubmit = function(event) {
        event.preventDefault();

        const angle = document.getElementById('angle').value;
        const A = document.getElementById('A').value;
        const I = document.getElementById('I').value;
        const BZ = document.getElementById('BZ').value;

        // Store the values in localStorage
        localStorage.setItem('angle', angle);
        localStorage.setItem('A', A);
        localStorage.setItem('I', I);
        localStorage.setItem('BZ', BZ);

        loading.style.display = 'flex';
        graphContent.style.display = 'none'; 

        this.submit();
    };
});


