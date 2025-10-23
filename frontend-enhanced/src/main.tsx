// src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

// Devtools shim: Some versions of React DevTools or browser extensions
// attempt to parse a semver string from the global hook and crash if
// it's missing or empty. Add a small, safe default during development.
if (import.meta.env?.DEV) {
  try {
    const hook = window as unknown as Record<string, unknown>;
    const g = hook.__REACT_DEVTOOLS_GLOBAL_HOOK__ as
      | { version?: unknown; [k: string]: unknown }
      | undefined;
    if (g) {
      const version = g.version;
      if (!version || typeof version !== "string" || version.trim() === "") {
        // provide a fallback semver string the devtools will accept
        (g as { version?: string }).version = "0.0.0";
      }
    }
  } catch (e) {
    // ignore errors in shim
    console.debug("devtools shim failed", e);
  }
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
