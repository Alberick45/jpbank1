// Customer search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('customerSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
});

// Transaction form validation
const transactionForm = document.getElementById('transactionForm');
if (transactionForm) {
    transactionForm.addEventListener('submit', function(e) {
        const amount = document.getElementById('amount').value;
        const accountNumber = document.getElementById('account_number').value;
        
        if (amount <= 0) {
            e.preventDefault();
            alert('Amount must be greater than 0');
            return;
        }
        
        if (accountNumber.length < 5) {
            e.preventDefault();
            alert('Please enter a valid account number');
            return;
        }
    });
}

// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    });
});

// Format currency inputs
document.querySelectorAll('input[type="number"][step="0.01"]').forEach(input => {
    input.addEventListener('blur', function() {
        if (this.value) {
            this.value = parseFloat(this.value).toFixed(2);
        }
    });
});

// Enable Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirm dangerous actions
document.addEventListener('DOMContentLoaded', function() {
    var dangerButtons = document.querySelectorAll('[data-confirm]');
    dangerButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm(this.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });
});

// Handle table sorting
document.addEventListener('DOMContentLoaded', function() {
    var tables = document.querySelectorAll('.table-sortable');
    tables.forEach(function(table) {
        var headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(function(header) {
            header.addEventListener('click', function() {
                var column = this.getAttribute('data-sort');
                var rows = Array.from(table.querySelectorAll('tbody tr'));
                var isAsc = this.classList.contains('asc');
                
                // Remove sort classes from all headers
                headers.forEach(h => h.classList.remove('asc', 'desc'));
                
                // Sort rows
                rows.sort(function(a, b) {
                    var aVal = a.querySelector(`td[data-${column}]`).getAttribute(`data-${column}`);
                    var bVal = b.querySelector(`td[data-${column}]`).getAttribute(`data-${column}`);
                    
                    if (aVal < bVal) return isAsc ? 1 : -1;
                    if (aVal > bVal) return isAsc ? -1 : 1;
                    return 0;
                });
                
                // Update sort direction
                this.classList.add(isAsc ? 'desc' : 'asc');
                
                // Reorder rows
                var tbody = table.querySelector('tbody');
                rows.forEach(row => tbody.appendChild(row));
            });
        });
    });
});

// Handle form validation
document.addEventListener('DOMContentLoaded', function() {
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Handle password visibility toggle
document.addEventListener('DOMContentLoaded', function() {
    var toggleButtons = document.querySelectorAll('.password-toggle');
    toggleButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var input = document.querySelector(this.getAttribute('data-target'));
            var icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
});
