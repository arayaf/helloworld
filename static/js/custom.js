// Custom JavaScript for STEM Learning Platform

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Quiz functionality
    const quizForms = document.querySelectorAll('form[data-quiz]');
    quizForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const quizId = form.dataset.quiz;
            
            // Show loading spinner
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
            submitBtn.disabled = true;
            
            // Submit quiz via AJAX
            fetch(`/stem/quiz/${quizId}/submit/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show result
                    showQuizResult(data);
                } else {
                    // Show errors
                    showQuizErrors(data.errors);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            })
            .finally(() => {
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
    });

    // Progress bar animations
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(function() {
            bar.style.width = width;
        }, 500);
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

function showQuizResult(data) {
    const resultHtml = `
        <div class="alert ${data.is_correct ? 'alert-success' : 'alert-danger'} mt-3">
            <h5><i class="fas fa-${data.is_correct ? 'check-circle' : 'times-circle'} me-2"></i>
                ${data.is_correct ? 'Correct!' : 'Incorrect'}
            </h5>
            <p class="mb-0">${data.explanation}</p>
            ${data.points_earned > 0 ? `<p class="mb-0 mt-2"><strong>Points earned: ${data.points_earned}</strong></p>` : ''}
        </div>
    `;
    
    const quizContainer = document.querySelector('.quiz-container');
    if (quizContainer) {
        quizContainer.insertAdjacentHTML('beforeend', resultHtml);
    }
}

function showQuizErrors(errors) {
    const errorHtml = `
        <div class="alert alert-danger mt-3">
            <h5><i class="fas fa-exclamation-triangle me-2"></i>Please fix the following errors:</h5>
            <ul class="mb-0">
                ${Object.values(errors).map(error => `<li>${error}</li>`).join('')}
            </ul>
        </div>
    `;
    
    const quizContainer = document.querySelector('.quiz-container');
    if (quizContainer) {
        quizContainer.insertAdjacentHTML('beforeend', errorHtml);
    }
}

// Utility functions
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}