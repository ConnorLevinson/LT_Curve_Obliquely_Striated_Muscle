document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const loading = document.getElementById('loading');
    const graphContent = document.getElementById('main');

    // Check if URL has parameters and set them
    const params = new URLSearchParams(window.location.search);
    if (params.has('angle')) {
        document.getElementById('angle').value = params.get('angle');
        document.getElementById('A').value = params.get('A');
        document.getElementById('I').value = params.get('I');
        document.getElementById('BZ').value = params.get('BZ');
    }

    form.onsubmit = function(event) {
        event.preventDefault();
    
        const angle = document.getElementById('angle').value;
        const A = document.getElementById('A').value;
        const I = document.getElementById('I').value;
        const BZ = document.getElementById('BZ').value;
    
        const baseUrl = window.location.origin + '/generate_graph'; // Adjust this to point to your Flask route
        const newUrl = `${baseUrl}?angle=${encodeURIComponent(angle)}&A=${encodeURIComponent(A)}&I=${encodeURIComponent(I)}&BZ=${encodeURIComponent(BZ)}`;
        window.location.href = newUrl;
    };
    
});

function printDocument() {
    window.print();
}

function generateShareableLink() {
    const angle = document.getElementById('angle').value;
    const A = document.getElementById('A').value;
    const I = document.getElementById('I').value;
    const BZ = document.getElementById('BZ').value;

    if (!angle || !A || !I || !BZ) {
        alert('Please make sure all values are entered before sharing.');
        return null;
    }

    const baseUrl = window.location.href.split('?')[0];
    const newUrl = `${baseUrl}?angle=${encodeURIComponent(angle)}&A=${encodeURIComponent(A)}&I=${encodeURIComponent(I)}&BZ=${encodeURIComponent(BZ)}`;
    return newUrl;
}

function shareLink() {
    const url = generateShareableLink();
    if (url) {
        navigator.clipboard.writeText(url).then(() => {
            alert('Link copied to clipboard!');
        }, (err) => {
            console.error('Could not copy text: ', err);
        });
    }
}

function printDocument() {
    window.print();
}




