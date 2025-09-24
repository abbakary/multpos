// Tanzania phone number validation and formatting
document.addEventListener('DOMContentLoaded', function() {
    // Find all phone input fields
    const phoneInputs = document.querySelectorAll('input[type="text"][name*="phone"], input[pattern*="255"]');
    
    phoneInputs.forEach(function(input) {
        // Add input event listener for real-time validation
        input.addEventListener('input', function(e) {
            let value = e.target.value;
            
            // Remove any non-digit characters except + and spaces
            value = value.replace(/[^\d+\s]/g, '');
            
            // Limit length based on format
            if (value.startsWith('+255')) {
                // International format: +255 XXX XXX XXX (max 16 chars)
                if (value.length > 16) {
                    value = value.substring(0, 16);
                }
            } else if (value.startsWith('0')) {
                // Local format: 0X XXX XXX XXX (max 14 chars)
                if (value.length > 14) {
                    value = value.substring(0, 14);
                }
            } else {
                // Prevent other formats
                if (value.length > 16) {
                    value = value.substring(0, 16);
                }
            }
            
            e.target.value = value;
        });
        
        // Add keydown event to prevent invalid characters
        input.addEventListener('keydown', function(e) {
            const allowedKeys = [
                'Backspace', 'Delete', 'Tab', 'Escape', 'Enter',
                'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
                'Home', 'End'
            ];
            
            // Allow control keys
            if (allowedKeys.includes(e.key) || e.ctrlKey || e.metaKey) {
                return;
            }
            
            // Allow digits, + and space
            if (!/[\d+\s]/.test(e.key)) {
                e.preventDefault();
            }
        });
        
        // Add paste event handler
        input.addEventListener('paste', function(e) {
            e.preventDefault();
            let paste = (e.clipboardData || window.clipboardData).getData('text');
            
            // Clean pasted content
            paste = paste.replace(/[^\d+\s]/g, '');
            
            // Apply length limits
            if (paste.startsWith('+255')) {
                paste = paste.substring(0, 16);
            } else if (paste.startsWith('0')) {
                paste = paste.substring(0, 14);
            } else {
                paste = paste.substring(0, 16);
            }
            
            e.target.value = paste;
            
            // Trigger input event for validation
            e.target.dispatchEvent(new Event('input', { bubbles: true }));
        });
    });
});