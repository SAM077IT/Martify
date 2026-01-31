#!/bin/bash
# Martify GitHub Issue Auto-Creator
# Repo: SAM077IT/Martify
# Requires: GitHub CLI (gh)

REPO="SAM077IT/Martify"

# Utility to create an issue with title and body
create_issue() {
  local TITLE="$1"
  local BODY="$2"
  echo "Creating issue: $TITLE"
  gh issue create --repo "$REPO" --title "$TITLE" --body "$BODY" --label "Day Task"
}

# ------------------------
# 🚀 DAY-BY-DAY ISSUE CREATION
# ------------------------

create_issue "Day 0 — Planning & repo init (prep)" "**Goal:** Set up repo and project planning.

**Checklist:**
- [ ] Create repo structure
- [ ] Add README, LICENSE, .gitignore
- [ ] Create Issues and Kanban board
- [ ] Define contribution & branch naming rules

**Acceptance Criteria:**
- Repo ready with README, LICENSE, and planning assets."

create_issue "Day 1 — Project skeleton & dev environment" "**Goal:** Create Django project and environment.

**Checklist:**
- [ ] Create virtualenv and install Django
- [ ] Start project: \`django-admin startproject martify\`
- [ ] Add requirements.txt and .env.example
- [ ] Run local dev server

**Acceptance Criteria:**
- Server runs locally at http://127.0.0.1:8000."

create_issue "Day 2 — App structure & core settings" "**Goal:** Create core apps and configure settings.

**Checklist:**
- [ ] Create apps: core, products, cart, orders, accounts, payments
- [ ] Setup INSTALLED_APPS and static/media
- [ ] Add base templates and root route

**Acceptance Criteria:**
- Home page loads; all apps registered."

create_issue "Day 3 — Database & models: Product model v1" "**Goal:** Implement Product and Category models.

**Checklist:**
- [ ] Add Product & Category models
- [ ] Run migrations
- [ ] Register in Django admin

**Acceptance Criteria:**
- Products & categories can be added via admin."

create_issue "Day 4 — Product list & detail views" "**Goal:** Implement product listing and detail pages.

**Checklist:**
- [ ] Create list and detail views
- [ ] Add pagination & category filters
- [ ] Add templates and URLs

**Acceptance Criteria:**
- Products can be browsed and opened individually."

create_issue "Day 5 — User accounts & auth" "**Goal:** Add authentication.

**Checklist:**
- [ ] Register/login/logout/password reset
- [ ] Profile model (optional)
- [ ] Templates for auth flows

**Acceptance Criteria:**
- Users can sign up and log in."

create_issue "Day 6 — Session-based cart" "**Goal:** Implement basic session cart.

**Checklist:**
- [ ] Add session cart logic (add/update/remove)
- [ ] Add cart page and total calculation
- [ ] Show cart item count in header

**Acceptance Criteria:**
- Can add and view items in session cart."

create_issue "Day 7 — Cart validation & UX" "**Goal:** Improve cart validation and UX.

**Checklist:**
- [ ] Validate inventory
- [ ] Allow quantity edits/removals
- [ ] Show correct subtotal and totals

**Acceptance Criteria:**
- Cart updates and validates correctly."

create_issue "Day 8 — DB-backed Cart models + merge-on-login" "**Goal:** Persist cart in DB and merge on login.

**Checklist:**
- [ ] Add Cart & CartItem models
- [ ] Merge session cart after login
- [ ] Add admin views for carts

**Acceptance Criteria:**
- Cart persists across sessions and merges properly."

create_issue "Day 9 — Orders & checkout flow (no payments)" "**Goal:** Convert cart to order flow.

**Checklist:**
- [ ] Add Order and OrderItem models
- [ ] Create checkout form
- [ ] Convert cart -> order

**Acceptance Criteria:**
- Checkout converts cart into an order successfully."

create_issue "Day 10 — Stripe integration" "**Goal:** Add Stripe payment (test mode).

**Checklist:**
- [ ] Install stripe and add keys
- [ ] Add checkout payment view
- [ ] Handle webhook to mark order paid

**Acceptance Criteria:**
- Test payments succeed and mark orders paid."

# You can continue adding days 11–30 here.
# (To keep script readable, stop at 10, then run again for remaining days.)

echo '✅ First 10 issues created successfully in SAM077IT/Martify!'
