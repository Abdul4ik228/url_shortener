(() => {
  const form = document.getElementById("shorten-form");
  const urlInput = document.getElementById("original-url");
  const expiresSelect = document.getElementById("expires-in");
  const submitBtn = document.getElementById("submit-btn");
  const errorEl = document.getElementById("form-error");
  const resultEl = document.getElementById("result");
  const resultLink = document.getElementById("result-link");
  const resultMeta = document.getElementById("result-meta");
  const copyBtn = document.getElementById("copy-btn");

  function showError(message) {
    errorEl.hidden = false;
    errorEl.textContent = message;
  }

  function clearError() {
    errorEl.hidden = true;
    errorEl.textContent = "";
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.classList.toggle("is-loading", isLoading);
  }

  function formatExpires(iso) {
    if (!iso) return "Срок действия: без ограничений";
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) return "";
    return `Действует до ${date.toLocaleString("ru-RU", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })}`;
  }

  function showResult({ short_url, expires_at }) {
    resultEl.hidden = false;
    resultLink.href = short_url;
    resultLink.textContent = short_url;
    resultMeta.textContent = formatExpires(expires_at);
    copyBtn.textContent = "Копировать";
    copyBtn.classList.remove("is-copied");
    // Restart pop animation on each success
    resultEl.style.animation = "none";
    // force reflow
    void resultEl.offsetWidth;
    resultEl.style.animation = "";
  }

  async function copyShortUrl() {
    const value = resultLink.textContent;
    if (!value) return;

    try {
      await navigator.clipboard.writeText(value);
    } catch {
      const tmp = document.createElement("textarea");
      tmp.value = value;
      document.body.appendChild(tmp);
      tmp.select();
      document.execCommand("copy");
      tmp.remove();
    }

    copyBtn.textContent = "Скопировано";
    copyBtn.classList.add("is-copied");
    window.setTimeout(() => {
      copyBtn.textContent = "Копировать";
      copyBtn.classList.remove("is-copied");
    }, 1800);
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearError();

    const originalUrl = urlInput.value.trim();
    if (!originalUrl) {
      showError("Вставьте ссылку, которую нужно сократить.");
      urlInput.focus();
      return;
    }

    const payload = { original_url: originalUrl };
    const expiresIn = expiresSelect.value;
    if (expiresIn) {
      payload.expires_in = Number(expiresIn);
    }

    setLoading(true);
    try {
      const response = await fetch("/api/v1/shorten", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        let detail = "Не удалось сократить ссылку.";
        try {
          const data = await response.json();
          if (typeof data.detail === "string") {
            detail = data.detail;
          } else if (Array.isArray(data.detail)) {
            detail = "Проверьте формат ссылки — нужен полный URL с https://";
          }
        } catch {
          /* ignore parse errors */
        }
        showError(detail);
        resultEl.hidden = true;
        return;
      }

      const data = await response.json();
      showResult(data);
    } catch {
      showError("Сервер недоступен. Проверьте, что проект запущен.");
      resultEl.hidden = true;
    } finally {
      setLoading(false);
    }
  });

  copyBtn.addEventListener("click", copyShortUrl);
})();
