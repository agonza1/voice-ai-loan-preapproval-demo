// Function to get URL parameters
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    const value = urlParams.get(name);
    return value ? decodeURIComponent(value) : null;
}

// Pre-fill form fields from URL parameters
function prefillForm() {
    console.log('Pre-filling form with URL parameters...');
    const legalName = getUrlParameter('legal_name');
    const email = getUrlParameter('email');
    const phone = getUrlParameter('phone');
    const zipCode = getUrlParameter('zip_code');
    
    console.log('URL parameters:', { legalName, email, phone, zipCode });
    
    if (legalName) {
        const legalNameField = document.getElementById('legal_name');
        if (legalNameField) {
            legalNameField.value = legalName;
            console.log('Pre-filled legal_name:', legalName);
        } else {
            console.warn('legal_name field not found');
        }
    }
    
    if (email) {
        const emailField = document.getElementById('email');
        if (emailField) {
            emailField.value = email;
            console.log('Pre-filled email:', email);
        } else {
            console.warn('email field not found');
        }
    }
    
    if (phone) {
        const phoneField = document.getElementById('phone');
        if (phoneField) {
            phoneField.value = phone;
            console.log('Pre-filled phone:', phone);
        } else {
            console.warn('phone field not found');
        }
    }
    
    if (zipCode) {
        const zipCodeField = document.getElementById('zip_code');
        if (zipCodeField) {
            zipCodeField.value = zipCode;
            console.log('Pre-filled zip_code:', zipCode);
        }
    }
}

// Function to initialize form
function initializeForm() {
    // Pre-fill form when page loads
    prefillForm();
    
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
}

// Run immediately if DOM is ready, otherwise wait for DOMContentLoaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeForm);
} else {
    // DOM is already ready
    initializeForm();
}
