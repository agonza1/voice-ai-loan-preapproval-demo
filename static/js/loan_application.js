document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loanForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/loan-application', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById('loanForm').style.display = 'none';
                    document.getElementById('success-message').style.display = 'block';
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                } else {
                    alert('Error: ' + (result.detail || 'Failed to submit application'));
                }
            } catch (error) {
                alert('Error submitting form: ' + error.message);
            }
        });
    }
});
