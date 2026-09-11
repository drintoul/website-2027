document.addEventListener("DOMContentLoaded", function () {
  populateConfig();
  initMobileNav();
  initActiveNav();
  initPlanForm();
  prefillPlanForm();
});

function populateConfig() {
  if (typeof window.SITE === "undefined") return;

  document.querySelectorAll("[data-config]").forEach(function (el) {
    var key = el.dataset.config;
    if (window.SITE[key] !== undefined) {
      el.textContent = window.SITE[key];
    }
  });

  var ctaButtons = document.querySelectorAll(".nav-cta .btn, .cta-primary");
  ctaButtons.forEach(function (btn) {
    if (window.SITE.primary_cta && !btn.textContent.trim()) {
      btn.textContent = window.SITE.primary_cta;
    }
  });
}

function initMobileNav() {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".primary-nav");
  if (!toggle || !nav) return;

  toggle.addEventListener("click", function () {
    var isOpen = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  document.querySelectorAll(".has-submenu > .nav-link").forEach(function (link) {
    link.addEventListener("click", function (e) {
      if (window.innerWidth <= 900) {
        e.preventDefault();
        var parent = link.parentElement;
        parent.classList.toggle("open");
      }
    });
  });
}

function initActiveNav() {
  var path = window.location.pathname.replace(/\/$/, "");
  document.querySelectorAll(".primary-nav a[href]").forEach(function (link) {
    var href = link.getAttribute("href").split("#")[0].replace(/\/$/, "");
    if (href === "/") href = "";
    if (href === path || (path && href && path.startsWith(href))) {
      link.setAttribute("aria-current", "page");
    }
  });
}

function prefillPlanForm() {
  var form = document.getElementById("plan-form");
  if (!form) return;

  var params = new URLSearchParams(window.location.search);
  function setField(name, value) {
    if (!value) return;
    var field = form.elements[name];
    if (!field) return;
    if (field.type === "checkbox") {
      field.checked = true;
    } else if (field.type === "radio") {
      var radios = form.elements[name];
      for (var i = 0; i < radios.length; i++) {
        if (radios[i].value === value) {
          radios[i].checked = true;
          break;
        }
      }
    } else {
      field.value = value;
    }
  }

  ["type", "status", "canada_only", "destination", "origin"].forEach(function (key) {
    setField(key, params.get(key));
  });
}

function initPlanForm() {
  var form = document.getElementById("plan-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var statusEl = form.querySelector(".form-status");
    statusEl.className = "form-status";
    statusEl.textContent = "";

    var endpoint = (window.SITE && window.SITE.api_endpoint) || "/api/plan";
    var formData = new FormData(form);

    fetch(endpoint, {
      method: "POST",
      body: formData,
    })
      .then(function (res) {
        if (!res.ok) throw new Error("Server responded with " + res.status);
        return res.json();
      })
      .then(function () {
        statusEl.classList.add("success");
        statusEl.textContent = "Thank you. Your trip request has been sent and Dave will be in touch soon.";
        form.reset();
      })
      .catch(function () {
        statusEl.classList.add("error");
        statusEl.textContent = "There was a problem sending your request. Please email or call using the contact details below.";
      });
  });
}
