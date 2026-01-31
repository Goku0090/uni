/**
 * UniSync Login Form Handler
 * Manages form submission, validation, and user feedback
 * 
 * Handles:
 * - Form submission with loading state
 * - Password visibility toggle
 * - Input validation feedback
 * - Error message auto-dismiss
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ UniSync Login JS - Initialized');

    const loginForm = document.getElementById('loginForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    /**
     * Form Submission Handler
     * Shows loading state and allows form to submit to Django backend
     */
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Validate inputs before submission
            if (!usernameInput || !usernameInput.value.trim()) {
                e.preventDefault();
                showFieldError(usernameInput, 'Username or email is required');
                return false;
            }

            if (!passwordInput || !passwordInput.value.trim()) {
                e.preventDefault();
                showFieldError(passwordInput, 'Password is required');
                return false;
            }

            // Show loading state
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
                submitBtn.style.pointerEvents = 'none';
                submitBtn.classList.add('opacity-70', 'cursor-not-allowed');
                
                if (btnText) {
                    btnText.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Logging in...';
                }
            }

            // Allow form to submit to Django backend
            return true;
        });
    }

    /**
     * Reset button state if page loads with form errors
     */
    window.addEventListener('load', function() {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.pointerEvents = 'auto';
            submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
            
            if (btnText) {
                btnText.innerHTML = '<i class="fas fa-sign-in-alt group-hover:translate-x-1 transition-transform"></i>Login to UniSync';
            }
        }
    });

    /**
     * Password Visibility Toggle
     * Show/hide password on button click
     */
    const togglePassword = document.getElementById('togglePassword');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function(e) {
            e.preventDefault();
            
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);

            const icon = this.querySelector('i');
            if (icon) {
                icon.className = type === 'text' ? 'fas fa-eye-slash' : 'fas fa-eye';
            }
        });
    }

    /**
     * Input Field Focus/Blur Effects
     */
    const inputs = document.querySelectorAll('#loginForm input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement?.classList.add('focused');
            clearFieldError(this);
        });

        input.addEventListener('blur', function() {
            this.parentElement?.classList.remove('focused');
        });

        // Clear error on input
        input.addEventListener('input', function() {
            if (this.value.trim()) {
                clearFieldError(this);
            }
        });
    });

    /**
     * Helper: Show Field Error
     */
    function showFieldError(field, message) {
        if (!field) return;
        
        // Add error styling
        field.classList.add('ring-2', 'ring-red-500', 'border-red-500');
        field.parentElement?.classList.add('ring-2', 'ring-red-500');

        // Show tooltip or message
        console.warn(`Form validation: ${message}`);
    }

    /**
     * Helper: Clear Field Error
     */
    function clearFieldError(field) {
        if (!field) return;
        
        field.classList.remove('ring-2', 'ring-red-500', 'border-red-500');
        field.parentElement?.classList.remove('ring-2', 'ring-red-500');
    }

    /**
     * Auto-dismiss error/success messages after 5 seconds
     */
    const messages = document.querySelectorAll('[class*="bg-red-500"], [class*="bg-green-500"]');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'all 0.5s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                if (msg.parentElement) {
                    msg.remove();
                }
            }, 500);
        }, 5000);
    });

    /**
     * Enter Key Submit
     * Allow login by pressing Enter in password field
     */
    if (passwordInput) {
        passwordInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (loginForm) {
                    loginForm.dispatchEvent(new Event('submit'));
                    loginForm.submit();
                }
            }
        });
    }

    /**
     * Remember Me Checkbox
     * Store preference in localStorage (optional enhancement)
     */
    const rememberCheckbox = document.querySelector('input[name="remember"]');
    if (rememberCheckbox && usernameInput) {
        // Load saved username if "Remember me" was checked
        const savedUsername = localStorage.getItem('unisync_saved_username');
        if (savedUsername) {
            usernameInput.value = savedUsername;
            rememberCheckbox.checked = true;
        }

        // Save username on successful submit
        loginForm?.addEventListener('submit', function() {
            if (rememberCheckbox.checked && usernameInput.value) {
                localStorage.setItem('unisync_saved_username', usernameInput.value);
            } else {
                localStorage.removeItem('unisync_saved_username');
            }
        });
    }

    console.log('✅ All login event listeners attached');
});
