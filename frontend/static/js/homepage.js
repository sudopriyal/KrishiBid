/**
 * KrishiBid Homepage Interactive Scripts
 * Handles:
 * 1. "The Middleman Killer" Interactive Margin Calculator
 * 2. Live Auction Countdown Clocks
 * 3. Category Filter for Live Lots
 * 4. Dual Journey Tab Switcher (Farmers vs Buyers)
 * 5. Quick-View Auction Modal logic
 */

document.addEventListener("DOMContentLoaded", function () {
    initMarginCalculator();
    initCountdownTimers();
    initCategoryFilters();
    initJourneyTabs();
    initQuickViewModal();
});

/* ==========================================================================
   1. "The Middleman Killer" Interactive Margin Calculator
   ========================================================================== */
function initMarginCalculator() {
    const cropData = {
        wheat: { name: "Sharbati Wheat", basePrice: 2800, unit: "Quintal", mandiDiscount: 0.28, krishiLift: 0.16 },
        tomato: { name: "Hybrid Tomato", basePrice: 4000, unit: "Quintal", mandiDiscount: 0.35, krishiLift: 0.20 },
        onion: { name: "Nashik Red Onion", basePrice: 2400, unit: "Quintal", mandiDiscount: 0.32, krishiLift: 0.18 },
        apple: { name: "Royal Delicious Apple", basePrice: 10000, unit: "Quintal", mandiDiscount: 0.30, krishiLift: 0.15 },
        pineapple: { name: "Queen Pineapple", basePrice: 4200, unit: "Quintal", mandiDiscount: 0.29, krishiLift: 0.17 },
        cotton: { name: "Shankar-6 Cotton", basePrice: 7200, unit: "Quintal", mandiDiscount: 0.26, krishiLift: 0.14 }
    };

    let selectedCropKey = "tomato";
    const slider = document.getElementById("calcQtySlider");
    const qtyValDisplay = document.getElementById("calcQtyDisplay");
    const cropButtons = document.querySelectorAll(".crop-btn-option");

    if (!slider) return;

    function updateCalculator() {
        const crop = cropData[selectedCropKey];
        const qty = parseInt(slider.value, 10);
        qtyValDisplay.textContent = `${qty} ${crop.unit}s`;

        const grossNominalValue = qty * crop.basePrice;

        // Traditional Mandi calculation:
        // Intermediary cuts: ~14% broker commission, 6% weighing/handling, 10% distressed discount = ~30% loss
        const mandiLossPercentage = crop.mandiDiscount;
        const mandiLoss = grossNominalValue * mandiLossPercentage;
        const mandiFarmerEarnings = grossNominalValue - mandiLoss;

        // KrishiBid Direct Auction calculation:
        // Direct bidding lift +15-20%, 0% broker fee, 1.5% escrow platform fee
        const krishiLiftAmount = grossNominalValue * crop.krishiLift;
        const escrowFee = (grossNominalValue + krishiLiftAmount) * 0.015;
        const krishiFarmerEarnings = grossNominalValue + krishiLiftAmount - escrowFee;

        // Extra profit into farmer's hands
        const extraProfit = krishiFarmerEarnings - mandiFarmerEarnings;
        const percentageGain = ((extraProfit / mandiFarmerEarnings) * 100).toFixed(1);

        // Update DOM elements
        const mandiBrokerElem = document.getElementById("mandiBrokerFee");
        const mandiDeductElem = document.getElementById("mandiOtherDeductions");
        const mandiTotalElem = document.getElementById("mandiNetPayout");

        const krishiBonusElem = document.getElementById("krishiBiddingSurge");
        const krishiFeeElem = document.getElementById("krishiEscrowFee");
        const krishiTotalElem = document.getElementById("krishiNetPayout");

        const extraMoneyDisplay = document.getElementById("calcExtraEarnings");
        const gainPercentDisplay = document.getElementById("calcGainPercent");

        if (mandiBrokerElem) mandiBrokerElem.textContent = `- ₹${Math.round(grossNominalValue * 0.14).toLocaleString("en-IN")}`;
        if (mandiDeductElem) mandiDeductElem.textContent = `- ₹${Math.round(mandiLoss - grossNominalValue * 0.14).toLocaleString("en-IN")}`;
        if (mandiTotalElem) mandiTotalElem.textContent = `₹${Math.round(mandiFarmerEarnings).toLocaleString("en-IN")}`;

        if (krishiBonusElem) krishiBonusElem.textContent = `+ ₹${Math.round(krishiLiftAmount).toLocaleString("en-IN")}`;
        if (krishiFeeElem) krishiFeeElem.textContent = `- ₹${Math.round(escrowFee).toLocaleString("en-IN")}`;
        if (krishiTotalElem) krishiTotalElem.textContent = `₹${Math.round(krishiFarmerEarnings).toLocaleString("en-IN")}`;

        if (extraMoneyDisplay) extraMoneyDisplay.textContent = `+ ₹${Math.round(extraProfit).toLocaleString("en-IN")}`;
        if (gainPercentDisplay) gainPercentDisplay.textContent = `+${percentageGain}% More Income`;
    }

    slider.addEventListener("input", updateCalculator);

    cropButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            cropButtons.forEach(b => b.classList.remove("active"));
            this.classList.add("active");
            selectedCropKey = this.getAttribute("data-crop");
            updateCalculator();
        });
    });

    updateCalculator();
}

/* ==========================================================================
   2. Live Auction Countdown Timers
   ========================================================================== */
function initCountdownTimers() {
    const timerElements = document.querySelectorAll(".live-countdown-timer");

    function tick() {
        const now = new Date().getTime();

        timerElements.forEach(el => {
            const endIso = el.getAttribute("data-end");
            if (!endIso) return;

            let endTime = new Date(endIso).getTime();
            if (isNaN(endTime)) {
                // If invalid date or demo, default to 4 hours from now
                endTime = now + (4 * 3600 * 1000);
            }

            const diff = endTime - now;

            if (diff <= 0) {
                el.innerHTML = `<span class="text-danger fw-bold"><i class="bi bi-clock-history"></i> Ended</span>`;
            } else {
                const hours = Math.floor(diff / (1000 * 60 * 60));
                const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const secs = Math.floor((diff % (1000 * 60)) / 1000);

                const hStr = hours < 10 ? "0" + hours : hours;
                const mStr = mins < 10 ? "0" + mins : mins;
                const sStr = secs < 10 ? "0" + secs : secs;

                el.innerHTML = `<i class="bi bi-hourglass-split"></i> ${hStr}h ${mStr}m ${sStr}s`;
            }
        });
    }

    tick();
    setInterval(tick, 1000);
}

/* ==========================================================================
   3. Category Filter for Live Lots
   ========================================================================== */
function initCategoryFilters() {
    const filterButtons = document.querySelectorAll(".cat-pill");
    const auctionCards = document.querySelectorAll(".auction-filterable-item");

    if (!filterButtons.length) return;

    filterButtons.forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            filterButtons.forEach(b => b.classList.remove("active"));
            this.classList.add("active");

            const category = this.getAttribute("data-category");

            auctionCards.forEach(card => {
                const cardCat = card.getAttribute("data-category");
                if (category === "all" || cardCat === category) {
                    card.style.display = "block";
                    card.style.opacity = "0";
                    setTimeout(() => {
                        card.style.opacity = "1";
                    }, 50);
                } else {
                    card.style.display = "none";
                }
            });
        });
    });
}

/* ==========================================================================
   4. Dual Journey Tab Switcher (Farmers vs Buyers)
   ========================================================================== */
function initJourneyTabs() {
    const tabFarmer = document.getElementById("tabBtnFarmer");
    const tabBuyer = document.getElementById("tabBtnBuyer");
    const stepsFarmer = document.getElementById("journeyStepsFarmer");
    const stepsBuyer = document.getElementById("journeyStepsBuyer");

    if (!tabFarmer || !tabBuyer || !stepsFarmer || !stepsBuyer) return;

    tabFarmer.addEventListener("click", function () {
        tabFarmer.classList.add("active");
        tabBuyer.classList.remove("active");
        stepsFarmer.classList.remove("d-none");
        stepsBuyer.classList.add("d-none");
    });

    tabBuyer.addEventListener("click", function () {
        tabBuyer.classList.add("active");
        tabFarmer.classList.remove("active");
        stepsBuyer.classList.remove("d-none");
        stepsFarmer.classList.add("d-none");
    });
}

/* ==========================================================================
   5. Quick-View Auction Modal
   ========================================================================== */
function initQuickViewModal() {
    const modalEl = document.getElementById("auctionQuickViewModal");
    if (!modalEl) return;

    const quickViewButtons = document.querySelectorAll(".btn-trigger-quickview");

    quickViewButtons.forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const crop = this.getAttribute("data-crop") || "Fresh Produce";
            const location = this.getAttribute("data-location") || "India";
            const farmer = this.getAttribute("data-farmer") || "Verified Farmer";
            const grade = this.getAttribute("data-grade") || "Grade A";
            const qty = this.getAttribute("data-qty") || "Lot";
            const startPrice = this.getAttribute("data-start") || "0.00";
            const currentBid = this.getAttribute("data-highest") || startPrice;
            const auctionId = this.getAttribute("data-id") || "";
            const buyerUrl = this.getAttribute("data-url") || "#";

            document.getElementById("modalCropName").textContent = crop;
            document.getElementById("modalLocation").textContent = location;
            document.getElementById("modalFarmer").textContent = farmer;
            document.getElementById("modalGrade").textContent = grade;
            document.getElementById("modalQty").textContent = qty;
            document.getElementById("modalStartPrice").textContent = `₹${parseFloat(startPrice).toFixed(2)}`;
            document.getElementById("modalCurrentBid").textContent = `₹${parseFloat(currentBid).toFixed(2)}`;

            const actionBtn = document.getElementById("modalActionBtn");
            if (actionBtn) {
                actionBtn.setAttribute("href", buyerUrl);
            }

            const bootstrapModal = new bootstrap.Modal(modalEl);
            bootstrapModal.show();
        });
    });
}
