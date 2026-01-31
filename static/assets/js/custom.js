
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
