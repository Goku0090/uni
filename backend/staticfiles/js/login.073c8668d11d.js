// Login page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Password toggle functionality
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);

            // Update icon
            const icon = this.querySelector('i');
            if (icon) {
                icon.className = type === 'text' ? 'fas fa-eye-slash' : 'fas fa-eye';
            }
        });
    }

    // Form elements
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput_elem = document.getElementById('password');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');

    // Helper functions for error handling (adapted for current HTML)
    function showFieldError(input, message) {
        const parent = input.parentElement;
        if (parent) {
            // Add error styling
            input.classList.add('border-red-500', 'focus:ring-red-500');
            // Create or update error message
            let errorMsg = parent.querySelector('.error-message');
            if (!errorMsg) {
                errorMsg = document.createElement('p');
                errorMsg.className = 'error-message text-red-500 text-sm mt-1';
                parent.appendChild(errorMsg);
            }
            errorMsg.textContent = message;
        }
    }

    function hideFieldError(input) {
        const parent = input.parentElement;
        if (parent) {
            input.classList.remove('border-red-500', 'focus:ring-red-500');
            const errorMsg = parent.querySelector('.error-message');
            if (errorMsg) {
                errorMsg.remove();
            }
        }
    }

    // Validation functions
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validateUsername(username) {
        if (validateEmail(username)) {
            return true;
        }
        const re = /^[a-zA-Z0-9_-]{3,30}$/;
        return re.test(username);
    }

    // Real-time validation on blur
    if (usernameInput) {
        usernameInput.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                showFieldError(this, 'Username or email is required');
            } else if (!validateUsername(this.value.trim())) {
                showFieldError(this, 'Please enter a valid username or email');
            } else {
                hideFieldError(this);
            }
        });

        // Clear errors on input
        usernameInput.addEventListener('input', function() {
            const parent = this.parentElement;
            if (parent && parent.querySelector('.error-message')) {
                hideFieldError(this);
            }
        });
    }

    if (passwordInput_elem) {
        passwordInput_elem.addEventListener('blur', function() {
            if (this.value === '') {
                showFieldError(this, 'Password is required');
            } else {
                hideFieldError(this);
            }
        });

        // Clear errors on input
        passwordInput_elem.addEventListener('input', function() {
            const parent = this.parentElement;
            if (parent && parent.querySelector('.error-message')) {
                hideFieldError(this);
            }
        });
    }

    // Form submission
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            let isValid = true;

            // Validate username
            if (!usernameInput || usernameInput.value.trim() === '') {
                if (usernameInput) showFieldError(usernameInput, 'Username or email is required');
                isValid = false;
            } else if (!validateUsername(usernameInput.value.trim())) {
                showFieldError(usernameInput, 'Please enter a valid username or email');
                isValid = false;
            } else {
                hideFieldError(usernameInput);
            }

            // Validate password
            if (!passwordInput_elem || passwordInput_elem.value === '') {
                if (passwordInput_elem) showFieldError(passwordInput_elem, 'Password is required');
                isValid = false;
            } else {
                hideFieldError(passwordInput_elem);
            }

            if (!isValid) {
                e.preventDefault();
                return false;
            }

            // Show loading state and allow form submission
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading', 'opacity-70');
            }
            if (btnText) {
                btnText.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Signing In...';
            }

            // Form will submit normally
            return true;
        });
    }

    // Enter key support
    if (usernameInput) {
        usernameInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (passwordInput_elem) passwordInput_elem.focus();
            }
        });
    }

    if (passwordInput_elem) {
        passwordInput_elem.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (loginForm) loginForm.submit();
            }
        });
    }

    // Remember me checkbox
    const rememberCheckbox = document.getElementById('remember');
    if (rememberCheckbox) {
        rememberCheckbox.addEventListener('change', function() {
            console.log('Remember me:', this.checked);
        });
    }

    // Auto-focus username field
    if (usernameInput) {
        usernameInput.focus();
    }
});
