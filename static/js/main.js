$(document).ready(function() {
    console.log('Document ready');

    // Clean up any stray modals and backdrops
    function cleanupModals() {
        $('.modal-backdrop').remove();
        $('body').removeClass('modal-open').css('padding-right', '');
        $('.modal').removeClass('show').hide();
    }

    // Initial cleanup
    cleanupModals();

    // Initialize Bootstrap components
    function initializeBootstrapComponents() {
        // Initialize tooltips
        $('[data-toggle="tooltip"]').tooltip();

        // Initialize popovers
        $('[data-toggle="popover"]').popover();

        // Initialize modals
        $('.modal').each(function() {
            var $modal = $(this);
            var modalId = $modal.attr('id');
            console.log('Initializing modal:', modalId);

            // Remove any existing event handlers
            $modal.off('.bs.modal');

            // Configure modal
            try {
                $modal.modal({
                    show: false,
                    backdrop: true,
                    keyboard: true,
                    focus: true
                });
            } catch (error) {
                console.error('Error initializing modal:', modalId, error);
            }

            // Add event handlers
            $modal.on({
                'show.bs.modal': function(e) {
                    console.log('Modal show event:', modalId);
                    // Ensure only one modal is open at a time
                    $('.modal').not(this).modal('hide');
                    // Ensure proper z-index
                    var zIndex = 1050 + (10 * $('.modal:visible').length);
                    $(this).css('z-index', zIndex);
                    setTimeout(function() {
                        $('.modal-backdrop').css('z-index', zIndex - 1);
                    }, 0);
                },
                'shown.bs.modal': function(e) {
                    console.log('Modal shown:', modalId);
                    // Focus Add to Library button
                    $(this).find('.modal-footer .btn-primary').focus();
                    // Ensure body has modal-open class
                    $('body').addClass('modal-open');
                },
                'hide.bs.modal': function(e) {
                    console.log('Modal hide event:', modalId);
                },
                'hidden.bs.modal': function(e) {
                    console.log('Modal hidden:', modalId);
                    // Clean up if this was the last modal
                    if ($('.modal:visible').length === 0) {
                        cleanupModals();
                    }
                },
                'error.bs.modal': function(e) {
                    console.error('Modal error:', modalId, e);
                    // Attempt recovery
                    cleanupModals();
                }
            });
        });
    }

    // Initialize components on page load
    initializeBootstrapComponents();

    // Handle modal triggers
    $(document).on('click', '[data-toggle="modal"]', function(e) {
        e.preventDefault();
        e.stopPropagation();

        var $trigger = $(this);
        var targetModal = $trigger.data('target');
        console.log('Modal trigger clicked:', {
            target: targetModal,
            button: $trigger.text().trim(),
            buttonParent: $trigger.parent().prop('tagName')
        });

        var $modal = $(targetModal);
        if ($modal.length) {
            try {
                // Hide any other open modals first
                $('.modal').not(targetModal).modal('hide');
                // Show the target modal
                $modal.modal('show');
            } catch (error) {
                console.error('Error showing modal:', error);
                // Fallback show method
                cleanupModals();
                $modal.show();
                $('body').addClass('modal-open').append('<div class="modal-backdrop fade show"></div>');
            }
        } else {
            console.error('Modal not found:', targetModal);
        }
    });

    // Handle modal close buttons
    $(document).on('click', '.modal .close, .modal .btn-secondary[data-dismiss="modal"]', function(e) {
        e.preventDefault();
        e.stopPropagation();

        var $modal = $(this).closest('.modal');
        var modalId = $modal.attr('id');
        console.log('Closing modal:', modalId);

        try {
            $modal.modal('hide');
        } catch (error) {
            console.error('Error hiding modal:', error);
            // Fallback hide method
            cleanupModals();
        }
    });

    // Handle escape key
    $(document).on('keydown', function(e) {
        if (e.key === 'Escape' && $('.modal:visible').length > 0) {
            var $modal = $('.modal:visible').last();
            console.log('Escape pressed, closing modal:', $modal.attr('id'));
            try {
                $modal.modal('hide');
            } catch (error) {
                console.error('Error closing modal with escape key:', error);
                cleanupModals();
            }
        }
    });

    // Prevent modal from closing when clicking modal content
    $(document).on('click', '.modal-content', function(e) {
        e.stopPropagation();
    });

    // Handle backdrop clicks
    $(document).on('click', '.modal', function(e) {
        if ($(e.target).hasClass('modal')) {
            var modalId = $(this).attr('id');
            console.log('Backdrop clicked, closing modal:', modalId);
            try {
                $(this).modal('hide');
            } catch (error) {
                console.error('Error closing modal on backdrop click:', error);
                cleanupModals();
            }
        }
    });

    // Re-initialize components after dynamic content loads
    $(document).ajaxComplete(function() {
        initializeBootstrapComponents();
    });

    // Handle window resize
    let resizeTimeout;
    $(window).on('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            // Adjust modal position on window resize
            $('.modal:visible').each(function() {
                $(this).modal('handleUpdate');
            });
        }, 250);
    });
});
