function setMessage(target, message, tone) {
  target.textContent = message;
  target.dataset.tone = tone;
  target.className = "status-message text-sm font-medium";

  if (tone === "success") {
    target.classList.add("text-emerald-300");
  } else if (tone === "error") {
    target.classList.add("text-rose-300");
  } else {
    target.classList.add("text-slate-300");
  }
}

function getApiBaseUrl() {
  const cached = window.__BACKEND_URL__;
  if (cached) {
    return cached;
  }

  return window.location.origin || "http://127.0.0.1:8000";
}

function initPasswordToggles() {
  document.querySelectorAll("[data-toggle-password]").forEach((button) => {
    button.addEventListener("click", () => {
      const wrapper = button.closest(".input-shell");
      const input = wrapper?.querySelector("input[type='password'], input[type='text']");
      const showIcon = button.querySelector("[data-icon='show']");
      const hideIcon = button.querySelector("[data-icon='hide']");

      if (!input || !showIcon || !hideIcon) {
        return;
      }

      const isHidden = input.type === "password";
      input.type = isHidden ? "text" : "password";
      showIcon.classList.toggle("hidden", !isHidden);
      hideIcon.classList.toggle("hidden", isHidden);
      button.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
      button.setAttribute("aria-pressed", String(isHidden));
    });
  });
}

async function submitAuthForm(form) {
  const status = form.querySelector("[data-status], [data-login-banner]");
  const button = form.querySelector("[type='submit']");
  const endpoint = form.dataset.endpoint;
  const redirectTo = form.dataset.redirect;
  const payload = Object.fromEntries(new FormData(form).entries());

  if (!endpoint) {
    setMessage(status, "Unable to submit this form right now.", "error");
    return;
  }

  try {
    const apiBaseUrl = await Promise.resolve(getApiBaseUrl());
    const requestUrl = new URL(endpoint, apiBaseUrl).toString();

    button.disabled = true;
    button.dataset.originalText = button.textContent;
    button.textContent = "Please wait...";
    setMessage(status, "Submitting request...", "info");

    const response = await fetch(requestUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data?.message || "Request failed");
    }

    if (form.dataset.mode === "register") {
      setMessage(status, data.message || "Registration complete.", "success");
      window.setTimeout(() => {
        window.location.href = redirectTo || "/login";
      }, 900);
      return;
    }

    if (data?.data?.access_token) {
      localStorage.setItem("access_token", data.data.access_token);
      localStorage.setItem("member", JSON.stringify(data.data));
    }

    setMessage(status, data.message || "Login successful.", "success");
  } catch (error) {
    setMessage(status, error.message || "Something went wrong.", "error");
  } finally {
    button.disabled = false;
    button.textContent = button.dataset.originalText || "Continue";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initPasswordToggles();

  document.querySelectorAll("[data-auth-form]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      submitAuthForm(form);
    });
  });

  const loginStatus = document.querySelector("[data-login-banner]");
  if (loginStatus && new URLSearchParams(window.location.search).get("registered") === "1") {
    setMessage(loginStatus, "Registration complete. You can log in now.", "success");
  }
});
