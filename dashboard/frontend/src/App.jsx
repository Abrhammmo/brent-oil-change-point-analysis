import { useEffect, useState } from "react";
import Dashboard from "./pages/Dashboard";

function App() {
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem("dashboard-theme");
    if (stored === "light" || stored === "dark") return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  });

  useEffect(() => {
    localStorage.setItem("dashboard-theme", theme);
    const root = document.documentElement;
    const body = document.body;
    root.classList.remove("light-theme", "dark-theme");
    body.classList.remove("light-theme", "dark-theme");
    root.classList.add(theme === "dark" ? "dark-theme" : "light-theme");
    body.classList.add(theme === "dark" ? "dark-theme" : "light-theme");
  }, [theme]);

  return (
    <div className="app-shell">
      <div className="theme-toggle-bar">
        <button
          type="button"
          className="theme-toggle-btn"
          onClick={() => setTheme((prev) => (prev === "dark" ? "light" : "dark"))}
        >
          Dark Mode: {theme === "dark" ? "On" : "Off"}
        </button>
      </div>
      <Dashboard theme={theme} />
    </div>
  );
}

export default App;
