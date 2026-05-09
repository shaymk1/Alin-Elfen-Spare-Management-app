// Spare Manager Frontend Utilities

document.addEventListener('DOMContentLoaded', function() {
    initializeUI();
});

function initializeUI() {
    // Add smooth transitions to alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0.9';
        }, 100);
    });

    // Initialize tooltips if any
    initializeTooltips();

    // Add form validation
    initializeFormValidation();
}

function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const text = event.target.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.style.position = 'absolute';
    tooltip.style.backgroundColor = 'var(--accent)';
    tooltip.style.color = 'var(--bg-primary)';
    tooltip.style.padding = '0.5rem 0.75rem';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '0.85rem';
    tooltip.style.zIndex = '1000';
    tooltip.style.pointerEvents = 'none';

    document.body.appendChild(tooltip);
    event.target.tooltip = tooltip;
}

function hideTooltip(event) {
    if (event.target.tooltip) {
        event.target.tooltip.remove();
        delete event.target.tooltip;
    }
}

function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', validateForm);
    });
}

function validateForm(event) {
    const form = event.target;
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');

    let isValid = true;
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = 'var(--error)';
            isValid = false;
        } else {
            input.style.borderColor = '';
        }
    });

    if (!isValid) {
        event.preventDefault();
        showNotification('Please fill out all required fields', 'error');
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.maxWidth = '400px';
    notification.style.zIndex = '10000';
    notification.style.animation = 'slideIn 0.3s ease-out';

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function toggleDetails(element) {
    const details = element.closest('.details-wrapper');
    if (details) {
        details.classList.toggle('open');
    }
}

// Export functions for template use
window.SpareManager = {
    showNotification,
    confirmDelete,
    formatDate,
    toggleDetails
};
