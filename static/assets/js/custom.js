
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



document.addEventListener("click", function (e) {
    const wishBtn = e.target.closest(".btn-icon-wish");
    if (!wishBtn) return;

    e.preventDefault(); // ⛔ stop <a> navigation

    const productId = wishBtn.dataset.productId;
    const icon = wishBtn.querySelector("i");

    fetch(`/user/wishlist/toggle/${productId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.in_wishlist) {
                wishBtn.classList.add("active added-wishlist");
                icon.classList.add("filled"); // optional CSS hook
            } else {
                wishBtn.classList.remove("active added-wishlist");
                icon.classList.remove("filled");
            }

            console.log("Wishlist count:", data.wishlist_count);
        })
        .catch(err => {
            console.error("Wishlist error:", err);
        });
});

// ─────────────────────────────────────────────────────────────────────
// QUICK VIEW ADD-TO-CART FIX
//
// PROBLEM: main.min.js initProductSingle() binds a jQuery click handler
// on ".add-cart" that calls e.preventDefault() — this stops the form
// submit event from ever firing. It also unhides a "View product" link.
//
// FIX STRATEGY:
// 1. Use a MutationObserver to detect when quick-view content is
//    injected into the DOM by Magnific Popup.
// 2. Immediately remove ALL jQuery click handlers from .add-cart
//    inside the quick-view form (killing the preventDefault).
// 3. Add our own click handler on the button that does AJAX add-to-cart
//    directly — no form submit needed.
// ─────────────────────────────────────────────────────────────────────

(function () {
    'use strict';

    function doQuickViewAddToCart(form, btn) {
        var url = form.action;
        var csrfToken = form.querySelector('[name=csrfmiddlewaretoken]');
        var formData = new FormData(form);
        var originalText = btn ? btn.textContent : 'Add to Cart';

        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Adding...';
        }

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken ? csrfToken.value : getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
            },
        })
        .then(function (r) {
            if (!r.ok && r.status !== 400) {
                throw new Error('Server error: ' + r.status);
            }
            return r.json();
        })
        .then(function (data) {
            // Update cart count badges everywhere
            document.querySelectorAll('.cart-count').forEach(function (badge) {
                badge.textContent = data.cart_count;
            });

            // Update cart popup subtotal
            var subtotalEl = document.querySelector('.dropdown-cart-total .cart-total-price');
            if (subtotalEl && data.cart_total !== undefined) {
                subtotalEl.textContent = '$' + parseFloat(data.cart_total).toFixed(2);
            }

            if (btn) {
                if (data.success) {
                    btn.textContent = 'Added ✓';
                    btn.classList.add('added');
                } else {
                    btn.textContent = data.errors ? data.errors[0] : 'Error';
                    btn.classList.add('error');
                }
                btn.disabled = false;
                setTimeout(function () {
                    btn.textContent = originalText;
                    btn.classList.remove('added', 'error');
                }, 2000);
            }
        })
        .catch(function (err) {
            console.error('Quick view cart add error:', err);
            if (btn) {
                btn.textContent = 'Failed';
                btn.disabled = false;
                btn.classList.add('error');
                setTimeout(function () {
                    btn.textContent = originalText;
                    btn.classList.remove('error');
                }, 2000);
            }
        });
    }

    function fixQuickViewAddCart() {
        var forms = document.querySelectorAll('.quickview-cart-form');
        forms.forEach(function (form) {
            var btn = form.querySelector('.add-cart');
            if (!btn) return;
            if (btn._quickviewFixed) return; // already fixed this button
            btn._quickviewFixed = true;

            // Remove ALL jQuery click event handlers that initProductSingle bound
            if (window.jQuery) {
                jQuery(btn).off('click');
            }

            // Add our own click handler directly on the button.
            // Since we removed jQuery's handler, this will be the only one.
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                doQuickViewAddToCart(form, btn);
            });
        });
    }

    // Watch for DOM changes — Magnific Popup injects quick-view HTML dynamically
    var observer = new MutationObserver(function (mutations) {
        var shouldFix = false;
        mutations.forEach(function (mutation) {
            mutation.addedNodes.forEach(function (node) {
                if (node.nodeType !== 1) return;
                if (node.classList && node.classList.contains('mfp-ajax-product')) {
                    shouldFix = true;
                }
                if (node.querySelector && node.querySelector('.quickview-cart-form')) {
                    shouldFix = true;
                }
            });
        });
        if (shouldFix) {
            // Wait for initProductSingle to finish (it runs in
            // ajaxContentAdded callback), then undo its click handler
            setTimeout(fixQuickViewAddCart, 200);
            // Also try again after a longer delay as a safety net
            setTimeout(fixQuickViewAddCart, 500);
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true,
    });

})();
