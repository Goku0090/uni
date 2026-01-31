
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const username = document.getElementById('id_username');
    const email = document.getElementById('id_email');
    const password = document.getElementById('id_password');

    let usernameTimeout, emailTimeout;

    const createError = (message, selector) => {
        const errorDiv = document.querySelector(selector);
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.color = '#ef4444';
        }
    };

    const createSuccess = (message, selector) => {
        const errorDiv = document.querySelector(selector);
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.color = '#10b981';
        }
    };

    const clearError = (selector) => {
        const errorDiv = document.querySelector(selector);
        if (errorDiv) {
            errorDiv.textContent = '';
        }
    };

    // Check username availability
    const checkUsernameAvailability = async (usernameValue) => {
        if (!usernameValue.trim() || usernameValue.length < 3) return;

        try {
            const response = await fetch(`/api/check-username/?username=${encodeURIComponent(usernameValue)}`);
            const data = await response.json();

            if (data.available) {
                createSuccess("✓ Username available", '.js-error-username');
            } else {
                createError("✗ Username already taken", '.js-error-username');
            }
        } catch (error) {
            console.error('Error checking username:', error);
        }
    };

    // Check email availability
    const checkEmailAvailability = async (emailValue) => {
        if (!emailValue.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue)) return;

        try {
            const response = await fetch(`/api/check-email/?email=${encodeURIComponent(emailValue)}`);
            const data = await response.json();

            if (data.available) {
                createSuccess("✓ Email available", '.js-error-email');
            } else {
                createError("✗ Email already registered", '.js-error-email');
            }
        } catch (error) {
            console.error('Error checking email:', error);
        }
    };

    // Real-time validation
    username.addEventListener('input', function() {
        clearTimeout(usernameTimeout);
        const value = this.value.trim();

        if (!value) {
            clearError('.js-error-username');
            return;
        }

        const usernamePattern = /^[\w.@+-]{1,150}$/;
        if (!usernamePattern.test(value)) {
            createError("Only letters, numbers, and @/./+/-/_ allowed.", '.js-error-username');
        } else {
            // Debounce the API call
            usernameTimeout = setTimeout(() => {
                checkUsernameAvailability(value);
            }, 500);
        }
    });

    email.addEventListener('input', function() {
        clearTimeout(emailTimeout);
        const value = this.value.trim();

        if (!value) {
            clearError('.js-error-email');
            return;
        }

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(value)) {
            createError("Enter a valid email address.", '.js-error-email');
        } else {
            // Debounce the API call
            emailTimeout = setTimeout(() => {
                checkEmailAvailability(value);
            }, 500);
        }
    });

    // Form submission validation
    form.addEventListener('submit', function (e) {
        let hasError = false;

        // Username validation
        const usernameValue = username.value.trim();
        if (!usernameValue) {
            createError("Username is required.", '.js-error-username');
            hasError = true;
        } else if (usernameValue.length < 3) {
            createError("Username must be at least 3 characters.", '.js-error-username');
            hasError = true;
        }

        // Email validation
        const emailValue = email.value.trim();
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailValue) {
            createError("Email is required.", '.js-error-email');
            hasError = true;
        } else if (!emailPattern.test(emailValue)) {
            createError("Enter a valid email address.", '.js-error-email');
            hasError = true;
        }

        // Password validation (basic check)
        const passwordValue = password.value;
        if (!passwordValue.trim()) {
            createError("Password is required.", '.js-error-password');
            hasError = true;
        }

        if (hasError) {
            e.preventDefault();
        }
    });
});
