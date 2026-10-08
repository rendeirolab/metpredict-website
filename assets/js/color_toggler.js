/*!
 * Color mode toggler, adapted from Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2024 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 *
 * The initial theme is applied by an inline script in <head> to avoid a flash
 * of the wrong theme; this script handles the theme menu.
 */

(() => {
    "use strict";

    const getStoredTheme = () => {
        try {
            return localStorage.getItem("theme");
        } catch (e) {
            return null;
        }
    };
    const setStoredTheme = (theme) => {
        try {
            localStorage.setItem("theme", theme);
        } catch (e) {}
    };

    // "light", "dark" or "auto" (follow the operating system)
    const getSelectedTheme = () => {
        const storedTheme = getStoredTheme();
        return storedTheme === "light" || storedTheme === "dark" ? storedTheme : "auto";
    };

    const setTheme = (theme) => {
        if (theme === "auto") {
            theme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        }
        document.documentElement.setAttribute("data-bs-theme", theme);
    };

    const showActiveTheme = (theme, focus = false) => {
        const themeSwitcher = document.querySelector("#bd-theme");
        const themeSwitcherText = document.querySelector("#bd-theme-text");
        const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`);

        if (!themeSwitcher || !btnToActive) {
            return;
        }

        document.querySelectorAll("[data-bs-theme-value]").forEach((element) => {
            element.classList.remove("active");
            element.setAttribute("aria-pressed", "false");
        });

        btnToActive.classList.add("active");
        btnToActive.setAttribute("aria-pressed", "true");
        themeSwitcher.setAttribute("aria-label", `${themeSwitcherText.textContent} (${theme})`);

        if (focus) {
            themeSwitcher.focus();
        }
    };

    setTheme(getSelectedTheme());

    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
        if (getSelectedTheme() === "auto") {
            setTheme("auto");
        }
    });

    const init = () => {
        showActiveTheme(getSelectedTheme());

        document.querySelectorAll("[data-bs-theme-value]").forEach((toggle) => {
            toggle.addEventListener("click", () => {
                const theme = toggle.getAttribute("data-bs-theme-value");
                setStoredTheme(theme);
                setTheme(theme);
                showActiveTheme(theme, true);
            });
        });
    };

    // The script is deferred, so the DOM may already be parsed
    if (document.readyState === "loading") {
        window.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
