
document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('id_password');
    const confirmPasswordInput = document.getElementById('id_confirm_password');
    const confirmErrorDiv = document.querySelector('.js-error-confirm');
    const passwordErrorDiv = document.querySelector('.js-error-password');
    const passwordRequirements = document.getElementById('passwordRequirements');

    if (!passwordRequirements) return; // Exit if requirements list doesn't exist

    const requirements = {
        length: {
            regex: /^.{8,}$/,
            element: passwordRequirements.querySelector('[data-requirement="length"]')
        },
        letter: {
            regex: /[A-Za-z]/,
            element: passwordRequirements.querySelector('[data-requirement="letter"]')
        },
        number: {
            regex: /\d/,
            element: passwordRequirements.querySelector('[data-requirement="number"]')
        },
        special: {
            regex: /[!@#$%^&*(),.?":{}|<>]/,
            element: passwordRequirements.querySelector('[data-requirement="special"]')
        }
    };

    function validatePassword(value) {
        let allValid = true;
        for (const key in requirements) {
            const requirement = requirements[key];
            const passed = requirement.regex.test(value);
            if (passed) {
                requirement.element.classList.remove('invalid');
                requirement.element.classList.add('valid');
            } else {
                requirement.element.classList.remove('valid');
                requirement.element.classList.add('invalid');
                allValid = false;
            }
        }
        return allValid;
    }

    function checkConfirmPassword() {
        const passwordValue = passwordInput.value;
        const confirmValue = confirmPasswordInput.value;

        if (confirmValue && passwordValue !== confirmValue) {
            confirmErrorDiv.textContent = "Passwords do not match.";
            confirmPasswordInput.classList.add('invalid');
            return false;
        } else if (confirmValue && passwordValue === confirmValue) {
            confirmErrorDiv.textContent = "";
            confirmPasswordInput.classList.remove('invalid');
            return true;
        }
        return true;
    }

    // Initial validation on page load
    validatePassword(passwordInput.value);
    checkConfirmPassword();

    // Real-time validation
    passwordInput.addEventListener('input', function () {
        validatePassword(this.value);
        checkConfirmPassword();
    });

    confirmPasswordInput.addEventListener('input', function () {
        checkConfirmPassword();
    });

    // Enhanced form validation
    const form = document.getElementById('registerForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const passwordValid = validatePassword(passwordInput.value);
            const confirmValid = checkConfirmPassword();

            if (!passwordValid || !confirmValid) {
                e.preventDefault();
                if (!passwordValid) {
                    passwordInput.focus();
                } else if (!confirmValid) {
                    confirmPasswordInput.focus();
                }
            }
        });
    }
});
