/* Dashboard light/dark theme toggle + language switcher (injected into the top navbar). */
(function () {
    "use strict";
    var root = document.documentElement;
    var fa = (root.getAttribute("lang") || "").indexOf("fa") === 0;
    var labels = fa
        ? { dark: "تم تاریک", light: "تم روشن", aria: "تغییر تم" }
        : { dark: "Dark mode", light: "Light mode", aria: "Toggle theme" };

    function current() { return root.getAttribute("data-theme") === "dark" ? "dark" : "light"; }

    function apply(theme, btn) {
        root.setAttribute("data-theme", theme);
        try { localStorage.setItem("dashboard-theme", theme); } catch (e) {}
        if (btn) {
            btn.textContent = theme === "dark" ? "☀️ " + labels.light : "🌙 " + labels.dark;
            btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
        }
    }

    function mount() {
        var holder = document.querySelector(".navbar-accounts .navbar-nav:last-of-type") ||
                     document.querySelector(".navbar-accounts");
        var li = document.createElement("li");
        li.className = "nav-item theme-toggle-item";
        var btn = document.createElement("button");
        btn.type = "button";
        btn.id = "theme-toggle";
        btn.className = "btn btn-sm btn-outline-light";
        btn.setAttribute("aria-label", labels.aria);
        btn.addEventListener("click", function () { apply(current() === "dark" ? "light" : "dark", btn); });
        li.appendChild(btn);
        if (holder) { holder.insertBefore(li, holder.firstChild); } else { document.body.appendChild(li); li.className += " theme-toggle-floating"; }
        apply(current(), btn);

        var form = document.getElementById("language-form");
        if (form && holder) {
            var li2 = document.createElement("li");
            li2.className = "nav-item language-item";
            li2.appendChild(form);
            form.hidden = false;
            holder.insertBefore(li2, holder.firstChild);
        }
    }

    if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", mount); } else { mount(); }
})();
