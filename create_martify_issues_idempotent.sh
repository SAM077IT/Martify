#!/usr/bin/env bash
# Idempotent Martify Issue Creator — creates only missing issues
# Repo: SAM077IT/Martify
# Requires: gh (GitHub CLI), authenticated with gh auth login

REPO="SAM077IT/Martify"
LABEL="Day Task"
MILESTONE="MVP Launch"
ASSIGNEE="@me"

# Ensure gh exists
if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh not found. Install GitHub CLI and run 'gh auth login'."
  exit 1
fi

# Ensure authenticated
if ! gh auth status >/dev/null 2>&1; then
  echo "ERROR: gh not authenticated. Run 'gh auth login' and try again."
  exit 1
fi

# Create label if missing
if ! gh label list --repo "$REPO" 2>/dev/null | grep -Fqx -- "$LABEL"; then
  echo "Creating label: $LABEL"
  gh label create "$LABEL" --repo "$REPO" --description "Daily roadmap task for Martify project" --color "0075FF"
fi

# Create milestone if missing
if ! gh milestone list --repo "$REPO" 2>/dev/null | awk -F'\t' '{print $1}' | grep -Fqx -- "$MILESTONE"; then
  echo "Creating milestone: $MILESTONE"
  gh milestone create "$MILESTONE" --repo "$REPO" --description "Milestone for Martify MVP launch"
fi

# fetch existing issue titles into a variable (JSON string)
EXISTING_JSON="$(gh issue list --repo "$REPO" --limit 200 --json title 2>/dev/null || echo '')"

issue_exists() {
  local title="$1"
  # simple exact-match check: look for the title string in the JSON list of titles
  if echo "$EXISTING_JSON" | grep -F "\"$title\"" >/dev/null 2>&1; then
    return 0  # exists
  else
    return 1  # not found
  fi
}

# Helper to create an issue (uses temp file to avoid quoting issues)
create_issue() {
  local TITLE="$1"
  local BODY="$2"

  if issue_exists "$TITLE"; then
    echo "Skipping (already exists): $TITLE"
    return 0
  fi

  local TMPFILE
  TMPFILE="$(mktemp /tmp/issue_body.XXXXXX.md 2>/dev/null || mktemp)"
  printf "%s\n" "$BODY" > "$TMPFILE"
  echo "Creating issue: $TITLE"
  gh issue create --repo "$REPO" --title "$TITLE" --body-file "$TMPFILE" --label "$LABEL" --assignee "$ASSIGNEE"

  rm -f "$TMPFILE"

  # refresh EXISTING_JSON so subsequent checks include newly created issues
  EXISTING_JSON="$(gh issue list --repo "$REPO" --limit 400 --json title 2>/dev/null || echo '')"
}

# ---------- Issues list (Day 0 -> Day 30) ----------
create_issue "Day 0 — Planning & repo init (prep)" "**Goal:** set up project repo, planning artifacts, and Issues board.

**Checklist:**
- [ ] Create GitHub repo named \`martify\`.
- [ ] Add \`README.md\` with project brief and MVP features.
- [ ] Add \`LICENSE\` and \`.gitignore\`.
- [ ] Create Issues (Day 0–Day 30) or import this document as issues.
- [ ] Create project board (Kanban) and populate initial columns.
- [ ] Create branch naming / contribution guidelines.

**Acceptance criteria:**
- Repository exists with README, LICENSE, and .gitignore. Issues for Days 0–30 are created or available. Project board is initialized."

create_issue "Day 1 — Project skeleton & dev environment" "**Goal:** create Django project & local dev environment.

**Checklist:**
- [ ] Create virtualenv and install initial dependencies (Django, psycopg2-binary, python-dotenv).
- [ ] \`django-admin startproject martify\` and initial commit.
- [ ] Add \`requirements.txt\`.
- [ ] Add \`.env.example\` and configure dotenv.
- [ ] (Optional) Add Dockerfile / docker-compose for local dev.

**Acceptance criteria:**
- \`manage.py runserver\` boots and shows Django default page locally."

create_issue "Day 2 — App structure & core settings" "**Goal:** create core apps and configure settings.

**Checklist:**
- [ ] Create apps: \`core\`, \`products\`, \`cart\`, \`orders\`, \`accounts\`, \`payments\`.
- [ ] Add apps to \`INSTALLED_APPS\`.
- [ ] Add base templates directory and root \`index\` template.
- [ ] Configure static & media settings for dev.
- [ ] Create base \`urls.py\` and connect app routes.

**Acceptance criteria:**
- Home page loads from the \`core\` app and each new app is registered."

create_issue "Day 3 — Database & models: Product model v1" "**Goal:** implement Product & Category models and admin.

**Checklist:**
- [ ] Create \`Category\` model with \`name\`, \`slug\`.
- [ ] Create \`Product\` model with \`title\`, \`slug\`, \`description\`, \`price\`, \`inventory\`, \`active\`, \`category\`, \`image\`.
- [ ] Register models in Django admin with basic \`list_display\`.
- [ ] Run \`makemigrations\` & \`migrate\`.

**Acceptance criteria:**
- Products and categories can be created via admin and exist in DB."

create_issue "Day 4 — Product list & detail views / templates" "**Goal:** show product listing and product detail pages.

**Checklist:**
- [ ] Implement product list view with pagination and category filter.
- [ ] Implement product detail view with product info and add-to-cart form.
- [ ] Create templates for list and detail pages.
- [ ] Add URL routes for list and detail.

**Acceptance criteria:**
- Can browse product list, filter by category, and open product detail pages."

create_issue "Day 5 — User accounts & auth" "**Goal:** accounts system with registration/login.

**Checklist:**
- [ ] Hook up Django auth views or custom auth views for register/login/logout.
- [ ] Implement password reset using console/email backend for dev.
- [ ] Create profile model (one-to-one) if needed.
- [ ] Add basic account templates.

**Acceptance criteria:**
- Sign up, login, logout work locally."

create_issue "Day 6 — Cart architecture decision & basic API (session-based cart)" "**Goal:** implement session-based cart for quick guest flows.

**Checklist:**
- [ ] Implement session-based cart utility (add, update, remove functions).
- [ ] Add view endpoints for add-to-cart and cart detail.
- [ ] Display cart item count in site header.
- [ ] Add simple cart template showing items and subtotal.

**Acceptance criteria:**
- Can add a product to the cart and see it in the cart page (session persists during browser session)."

create_issue "Day 7 — Cart: validations & UX polish" "**Goal:** add server-side validations and polish cart UX.

**Checklist:**
- [ ] Validate available inventory when adding/updating items.
- [ ] Ensure quantity limits and proper error messages.
- [ ] Allow item quantity edits and removals from cart page.
- [ ] Show cart subtotal and item-level totals.

**Acceptance criteria:**
- Cart prevents adding more than available inventory and updates totals correctly."

create_issue "Day 8 — DB-backed Cart models + merge-on-login" "**Goal:** persist carts in DB and merge session cart on login.

**Checklist:**
- [ ] Create \`Cart\` and \`CartItem\` models (cart.user nullable, cart.session_key optional).
- [ ] Implement logic to create/get cart for authenticated users and guest session.
- [ ] Implement merge logic and wire it to \`user_logged_in\` signal.
- [ ] Migrate DB and add basic admin for Cart.

**Acceptance criteria:**
- Cart items persist after login and session cart merges into user's DB cart."

create_issue "Day 9 — Orders & Checkout basic flow (no payments)" "**Goal:** convert cart to \`Order\`/\`OrderItem\` and capture checkout info.

**Checklist:**
- [ ] Create \`Order\` and \`OrderItem\` models (snapshot price, qty, status).
- [ ] Implement checkout view to capture shipping & billing details.
- [ ] On checkout submit, create an \`Order\` with \`OrderItem\`s and clear cart.
- [ ] Add order confirmation page.

**Acceptance criteria:**
- Checkout converts cart into an \`Order\` with correct line items and snapshots."

create_issue "Day 10 — Integrate Stripe (payment)" "**Goal:** integrate Stripe payments (test mode) and update order status.

**Checklist:**
- [ ] Add \`stripe\` to dependencies and set test keys in \`.env\`.
- [ ] Implement Stripe PaymentIntent or Checkout Session flow.
- [ ] Create webhook endpoint to listen for successful payments and mark \`Order.paid=True\`.
- [ ] Test payments with Stripe CLI or test webhook handling.

**Acceptance criteria:**
- Test payments mark orders as paid and webhook handling updates order status."

create_issue "Day 11 — Order confirmation & emails" "**Goal:** send transactional order confirmation emails and build order detail page.

**Checklist:**
- [ ] Configure email backend for dev (console) and prod provider env vars.
- [ ] Send order confirmation email after successful payment.
- [ ] Implement order detail page for customers to view order status.

**Acceptance criteria:**
- Confirmation email is sent in dev and order detail page shows accurate data."

create_issue "Day 12 — Admin improvements & order management" "**Goal:** improve Django admin for orders and products.

**Checklist:**
- [ ] Add admin list displays and filters for \`Order\` (status, date, user).
- [ ] Add admin actions to change status (mark shipped, refunded).
- [ ] Improve product admin (search, filters, inline images).

**Acceptance criteria:**
- Admin can view and manage orders and products efficiently."

create_issue "Day 13 — Product images & media handling" "**Goal:** support multiple product images and media serving.

**Checklist:**
- [ ] Add \`ProductImage\` model or multiple image handling.
- [ ] Implement image upload in admin and product edit pages.
- [ ] Configure \`MEDIA_URL\`/ \`MEDIA_ROOT\` and dev serving.
- [ ] Add production notes for S3 config.

**Acceptance criteria:**
- Product pages display image gallery and images upload works in admin."

create_issue "Day 14 — Search & filtering" "**Goal:** add search and filtering to product lists.

**Checklist:**
- [ ] Implement search by title/description (query param \`q\`).
- [ ] Add filters for category and price range.
- [ ] Add pagination and preserve query params across pages.

**Acceptance criteria:**
- Users can search products and combine filters; results match expectations."

create_issue "Day 15 — Reviews & Ratings (optional)" "**Goal:** add product reviews and average rating.

**Checklist:**
- [ ] Create \`Review\` model (user, product, rating, text, moderated boolean).
- [ ] Add review form on product detail page for authenticated users.
- [ ] Display reviews and average rating.

**Acceptance criteria:**
- Authenticated users can submit reviews; ratings aggregate correctly."

create_issue "Day 16 — Promotions & coupons" "**Goal:** implement coupon model and cart discount logic.

**Checklist:**
- [ ] Create \`Coupon\` model (code, type, amount, expiry, limits).
- [ ] Add coupon apply/remove UI on cart/checkout.
- [ ] Ensure coupon validation and usage counting.

**Acceptance criteria:**
- Applying valid coupon changes totals correctly; invalid coupons are rejected."

create_issue "Day 17 — Shipping & tax basics" "**Goal:** add shipping options and simple tax logic.

**Checklist:**
- [ ] Implement shipping methods (flat, free over X).
- [ ] Add tax calculation stub (state-based or percentage).
- [ ] Surface shipping & tax on checkout and update totals.

**Acceptance criteria:**
- Checkout shows shipping options and taxes; totals reflect both correctly."

create_issue "Day 18 — User addresses & saved profiles" "**Goal:** allow users to save and reuse shipping addresses.

**Checklist:**
- [ ] Create \`Address\` model linked to user.
- [ ] Add address management UI in account/profile pages.
- [ ] Allow selecting saved address at checkout.

**Acceptance criteria:**
- Users can save addresses and select one during checkout."

create_issue "Day 19 — Responsive UI & basic styling" "**Goal:** make the site responsive and visually cleaner.

**Checklist:**
- [ ] Integrate CSS framework (Tailwind or Bootstrap).
- [ ] Ensure header/nav/cart are mobile-friendly.
- [ ] Make product grid responsive and image scaling correct.

**Acceptance criteria:**
- Key pages are usable on mobile widths."

create_issue "Day 20 — Tests: unit & integration" "**Goal:** add automated tests for critical flows.

**Checklist:**
- [ ] Add tests for Product model and views.
- [ ] Add tests for cart add/update/remove flows.
- [ ] Add tests for checkout -> order conversion and webhook handling.
- [ ] Configure test runner in CI.

**Acceptance criteria:**
- Core tests exist and pass locally and in CI."

create_issue "Day 21 — Performance & caching" "**Goal:** reduce query counts and add caching for heavy views.

**Checklist:**
- [ ] Add \`select_related\` / \`prefetch_related\` where needed.
- [ ] Add Redis caching for product list and fragments.
- [ ] Add DB indexes for slug and category fields.

**Acceptance criteria:**
- Product list/detail pages show fewer DB queries and faster response."

create_issue "Day 22 — Analytics, logging & monitoring" "**Goal:** integrate basic analytics and server error monitoring.

**Checklist:**
- [ ] Add GA4 snippet or measurement for page views/events.
- [ ] Track add-to-cart, checkout-start, purchase events.
- [ ] Add server logging and configure Sentry (or equivalent).

**Acceptance criteria:**
- Events are visible in analytics and server errors are captured in logs."

create_issue "Day 23 — SEO & sitemaps" "**Goal:** add basic SEO improvements and sitemap.

**Checklist:**
- [ ] Add meta title & description tags to product pages.
- [ ] Add \`og:\` social tags and canonical tags.
- [ ] Generate \`sitemap.xml\` for product and category pages.
- [ ] Add \`robots.txt\`.

**Acceptance criteria:**
- Sitemap is accessible and key pages have meta tags."

create_issue "Day 24 — CI/CD & deployment prep" "**Goal:** create CI pipeline and prepare for deployment.

**Checklist:**
- [ ] Add GitHub Actions workflow to run tests on PRs.
- [ ] Add Dockerfile and build steps for production image.
- [ ] Document deployment steps in DEPLOY.md.

**Acceptance criteria:**
- CI runs on push and tests are executed; Docker build succeeds."

create_issue "Day 25 — Deploy to staging" "**Goal:** deploy the app to a staging environment and run smoke tests.

**Checklist:**
- [ ] Deploy to chosen provider with staging settings.
- [ ] Configure DB, static files, and media storage for staging.
- [ ] Perform manual smoke tests (browse, add to cart, checkout test flow).

**Acceptance criteria:**
- Staging URL is live and basic flows work end-to-end."

create_issue "Day 26 — Domain, SSL & email for prod" "**Goal:** configure production domain, HTTPS, and transactional email.

**Checklist:**
- [ ] Purchase domain and add DNS records.
- [ ] Configure SSL (Let's Encrypt or provider).
- [ ] Configure email provider (SendGrid/Mailgun) and add env vars.

**Acceptance criteria:**
- Domain resolves to app, site is HTTPS, and emails can be sent from prod."

create_issue "Day 27 — Security & compliance" "**Goal:** harden security settings and prepare basic legal pages.

**Checklist:**
- [ ] Set \`SECURE_SSL_REDIRECT\`, \`SESSION_COOKIE_SECURE\`, \`CSRF_COOKIE_SECURE\` in prod settings.
- [ ] Configure \`ALLOWED_HOSTS\` and Content Security Policy notes.
- [ ] Draft privacy policy and terms of service templates.

**Acceptance criteria:**
- Security settings applied to production config and legal docs drafted."

create_issue "Day 28 — Customer flows & UX polish" "**Goal:** test and polish user journeys and fix UX issues.

**Checklist:**
- [ ] Manually test flows (browse -> add to cart -> checkout -> payment -> order email).
- [ ] Address form validation, edge cases, and usability bugs.
- [ ] Improve error messages and accessibility fixes.

**Acceptance criteria:**
- All major user flows work smoothly on staging and critical UX issues are addressed."

create_issue "Day 29 — Launch checklist & marketing basics" "**Goal:** prepare launch assets and basic marketing plan.

**Checklist:**
- [ ] Prepare homepage hero and launch promotional banner.
- [ ] Prepare social handles, announcement copy, and mailing list sign-up.
- [ ] Prepare initial product feed and featured categories.

**Acceptance criteria:**
- Marketing assets and copy are ready for launch; social handles reserved."

create_issue "Day 30 — Launch & post-launch monitoring" "**Goal:** push production release and monitor the site.

**Checklist:**
- [ ] Deploy release to production.
- [ ] Run smoke tests and a test purchase in production.
- [ ] Monitor logs, errors, and analytics for first-day metrics.
- [ ] Prepare rollback steps in case of critical failures.

**Acceptance criteria:**
- Production site is live, orders flowing, and monitoring is in place."

echo "Done — created missing issues (or skipped existing) for $REPO."
