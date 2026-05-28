/**
 * cart.js – Shared AJAX cart remove for header popup & mobile sticky bar.
 *
 * Works with:
 *   - Cart page  (.martify-cart-page)  inline remove forms
 *   - Header dropdown cart popup        (.cart-dropdown)
 *
 * Both server-side views already return JSON when X-Requested-With: XMLHttpRequest.
 */

(function () {
    'use strict';

    // ── CSRF helper (reuse if already defined in custom.js) ──────────────
    if (typeof getCookie !== 'function') {
        window.getCookie = function (name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.startsWith(name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        };
    }

    // ── Update every cart-count badge in header / sticky bar ─────────────
    function updateCartCount(count) {
        document.querySelectorAll('.cart-count').forEach(function (badge) {
            badge.textContent = count;
        });
    }

    // ── Update cart popup subtotal text ──────────────────────────────────
    function updatePopupSubtotal(total) {
        var subtotalEl = document.querySelector('.dropdown-cart-total .cart-total-price');
        if (subtotalEl) {
            subtotalEl.textContent = '$' + parseFloat(total).toFixed(2);
        }
    }

    // ── Show empty cart message inside popup ─────────────────────────────
    function showPopupEmptyMessage() {
        var container = document.querySelector('.dropdown-cart-products');
        if (!container) return;
        container.innerHTML = '<p class="text-center">Your cart is empty</p>';
    }

    // ─────────────────────────────────────────────────────────────────────
    // HEADER / POPUP CART  –  AJAX remove
    // ─────────────────────────────────────────────────────────────────────
    document.addEventListener('submit', function (e) {
        var form = e.target.closest('.cart-dropdown .cart-product-remove');
        if (!form) return;

        e.preventDefault();

        // Walk up to the .product wrapper so we can remove it from DOM
        var productEl = form.closest('.cart-dropdown .product');
        var url = form.action;
        var csrfToken = form.querySelector('[name=csrfmiddlewaretoken]');

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken ? csrfToken.value : getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
            },
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            // Slide-out animation then remove from DOM
            if (productEl) {
                productEl.style.transition = 'opacity 0.3s, max-height 0.3s';
                productEl.style.opacity = '0';
                productEl.style.maxHeight = productEl.offsetHeight + 'px';
                // Force reflow
                productEl.offsetHeight;
                productEl.style.maxHeight = '0';
                productEl.style.overflow = 'hidden';
                productEl.style.padding = '0';
                productEl.style.margin = '0';

                setTimeout(function () { productEl.remove(); }, 300);
            }

            // Update subtotal in popup
            if (data.cart_total !== undefined) {
                updatePopupSubtotal(data.cart_total);
            }

            // Update badge count everywhere
            updateCartCount(data.cart_count);

            // If cart is now empty, show empty message
            if (data.cart_count === 0) {
                setTimeout(showPopupEmptyMessage, 320);
            }

            // Also update cart-page summary elements (if user is on cart page)
            updateCartPageSummary(data);
        })
        .catch(function (err) { console.error('Cart remove error:', err); });
    });

    // ── Delegate: clicking inside .cart-dropdown ─────────────────────────
    // (also catches dynamically-added forms)
    // NOTE: quickview-cart-form is handled by custom.js via click interception

    // ─────────────────────────────────────────────────────────────────────
    // SHARED HELPERS
    // ─────────────────────────────────────────────────────────────────────

    function updateCartPageSummary(data) {
        if (data.cart_total !== undefined) {
            var subtotalEl = document.querySelector('.cart-summary-subtotal');
            if (subtotalEl) subtotalEl.textContent = '$' + parseFloat(data.cart_total).toFixed(2);
        }
        if (data.cart_total_after_discount !== undefined) {
            var totalEl = document.querySelector('.cart-summary-total');
            if (totalEl) totalEl.textContent = '$' + parseFloat(data.cart_total_after_discount).toFixed(2);
        }
        if (data.cart_discount !== undefined) {
            var discountRow = document.querySelector('.cart-summary-discount-row');
            var discountVal = parseFloat(data.cart_discount);
            if (discountVal > 0) {
                if (discountRow) {
                    var el = discountRow.querySelector('.cart-summary-discount');
                    if (el) el.textContent = '-$' + discountVal.toFixed(2);
                }
            } else {
                if (discountRow) discountRow.remove();
            }
        }
    }

    // Expose so cart.html inline script can reuse
    window.CartAjax = {
        updateCartCount: updateCartCount,
        updateCartPageSummary: updateCartPageSummary,
    };

})();
