import React, { useEffect, useState, useCallback } from "react";
import { API_BASE } from "../services/api";

type ServiceKey = "ndvi" | "soil" | "weather" | "crops" | "water" | "pests";

const SERVICES: Record<ServiceKey, { label: string; url: string }> = {
  // Keep the base URL only; checks will try sensible health/debug candidates.
  ndvi: { label: "NDVI", url: `${API_BASE.ndvi}` },
  soil: { label: "Soil", url: `${API_BASE.soil}` },
  weather: { label: "Weather", url: `${API_BASE.weather}` },
  crops: { label: "Crops", url: `${API_BASE.crops}` },
  water: { label: "Water", url: `${API_BASE.water}` },
  pests: { label: "Pests", url: `${API_BASE.pests}` },
};

const TIMEOUT_MS = 5000;

// Build candidate endpoints safely to avoid double-prefix issues.
const joinUrl = (base: string, path: string) => {
  if (!base) return path;
  return `${base.replace(/\/+$/, "")}/${path.replace(/^\/+/, "")}`;
};

const SERVICE_NAME_MAP: Record<ServiceKey, string> = {
  ndvi: "ndvi",
  soil: "soil",
  weather: "weather",
  crops: "crop",
  water: "water",
  pests: "pest",
};

const makeCandidates = (base: string, name: string) => {
  // Try common health/debug locations in order of likelihood
  return [
    joinUrl(base, `api/${name}/debug`),
    joinUrl(base, `api/${name}/health`),
    joinUrl(base, `api/health`),
    joinUrl(base, `health`),
    joinUrl(base, `debug`),
    base,
  ];
};

const checkHealth = async (url: string) => {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(id);
    if (!res.ok) {
      return { ok: false, status: res.status, statusText: res.statusText };
    }
    const json = await res.json().catch(() => null);
    return { ok: true, status: res.status, statusText: res.statusText, json };
  } catch (e: unknown) {
    clearTimeout(id);
    const isAbort =
      typeof e === "object" &&
      e !== null &&
      "name" in e &&
      (e as { name: unknown }).name === "AbortError";
    if (isAbort) {
      return { ok: false, status: 408, statusText: "Timeout" };
    }
    let msg = "Network error";
    if (typeof e === "string") {
      msg = e;
    } else if (e instanceof Error) {
      msg = e.message;
    } else if (
      typeof e === "object" &&
      e !== null &&
      "message" in e &&
      typeof (e as { message?: unknown }).message === "string"
    ) {
      msg = (e as { message: string }).message;
    }
    return { ok: false, status: 0, statusText: msg };
  }
};

const ServicesStatus: React.FC = () => {
  const [state, setState] = useState<
    Record<
      ServiceKey,
      { healthy: boolean; lastChecked?: string; details?: string }
    >
  >(() => {
    const s: Partial<
      Record<
        ServiceKey,
        { healthy: boolean; lastChecked?: string; details?: string }
      >
    > = {};
    (Object.keys(SERVICES) as ServiceKey[]).forEach((k) => {
      s[k] = { healthy: false, lastChecked: undefined, details: undefined };
    });
    return s as Record<
      ServiceKey,
      { healthy: boolean; lastChecked?: string; details?: string }
    >;
  });

  const refresh = useCallback(async () => {
    const keys = Object.keys(SERVICES) as ServiceKey[];
    await Promise.all(
      keys.map(async (k) => {
        const info = SERVICES[k];
        const candidates = makeCandidates(info.url, SERVICE_NAME_MAP[k]);
        let ok = false;
        let details: unknown = undefined;
        for (const url of candidates) {
          const res = await checkHealth(url);
          if (res.ok) {
            ok = true;
            details = res.json ?? "OK";
            break;
          } else {
            // keep the last error detail if none succeed
            details = `${res.status} ${res.statusText}`;
          }
        }

        setState((prev) => ({
          ...prev,
          [k]: {
            healthy: ok,
            lastChecked: new Date().toISOString(),
            details: ok
              ? typeof details === "string"
                ? details
                : JSON.stringify(details)
              : details,
          },
        }));
      })
    );
  }, []);

  // Debug data state and fetcher
  const [debugVisible, setDebugVisible] = useState(false);
  const [debugData, setDebugData] = useState<
    Partial<Record<ServiceKey, unknown>>
  >({});

  const fetchDebugForService = useCallback(async (k: ServiceKey) => {
    const endpoints = makeCandidates(SERVICES[k].url, SERVICE_NAME_MAP[k]);
    for (const url of endpoints) {
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), TIMEOUT_MS * 2);
      try {
        const res = await fetch(url, { signal: controller.signal });
        clearTimeout(id);
        if (!res.ok) {
          // try next endpoint
          continue;
        }
        const json = await res.json().catch(() => null);
        setDebugData((prev) => ({
          ...prev,
          [k]: json ?? `${res.status} ${res.statusText}`,
        }));
        return;
      } catch {
        clearTimeout(id);
        // try next endpoint
        continue;
      }
    }
    setDebugData((prev) => ({
      ...prev,
      [k]: { error: "No debug endpoint responded" },
    }));
  }, []);

  const fetchAllDebug = useCallback(async () => {
    const keys = Object.keys(SERVICES) as ServiceKey[];
    setDebugData({});
    await Promise.all(keys.map((k) => fetchDebugForService(k)));
    setDebugVisible(true);
  }, [fetchDebugForService]);

  useEffect(() => {
    // initial refresh and then poll every 10s
    refresh();
    const t = setInterval(refresh, 10000);
    return () => clearInterval(t);
  }, [refresh]);

  return (
    <div className="bg-white p-4 rounded-lg shadow border w-full max-w-2xl">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-700">Services Status</h3>
        <div className="flex items-center gap-2">
          <button
            onClick={refresh}
            className="text-xs px-2 py-1 bg-gray-100 rounded border hover:bg-gray-50"
          >
            Refresh
          </button>
          <button
            onClick={fetchAllDebug}
            className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded border hover:bg-blue-50"
          >
            Fetch Debug
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2">
        {(Object.keys(SERVICES) as ServiceKey[]).map((k) => {
          const info = SERVICES[k];
          const st = state[k];
          return (
            <div
              key={k}
              className="flex items-center justify-between p-2 rounded border border-gray-100 bg-white"
            >
              <div className="flex items-center gap-3">
                <span
                  className={`w-3 h-3 rounded-full inline-block ${
                    st && st.healthy ? "bg-green-500" : "bg-red-400"
                  }`}
                />
                <div>
                  <div className="text-sm font-medium text-gray-800">
                    {info.label}
                  </div>
                  <div className="text-xs text-gray-500">{info.url}</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs font-medium text-gray-700">
                  {st && st.healthy ? "Healthy" : "Down"}
                </div>
                <div className="text-xs text-gray-400">
                  {st && st.lastChecked
                    ? new Date(st.lastChecked).toLocaleTimeString()
                    : "-"}
                </div>
              </div>
            </div>
          );
        })}
      </div>
      {/* Debug panel */}
      {debugVisible && (
        <div className="mt-4 p-3 bg-gray-50 border rounded">
          <h4 className="text-sm font-semibold mb-2">Debug Output</h4>
          <div className="space-y-3">
            {(Object.keys(SERVICES) as ServiceKey[]).map((k) => (
              <div key={k} className="text-xs">
                <div className="font-medium">{SERVICES[k].label}</div>
                <pre className="mt-1 p-2 bg-white border rounded text-[11px] overflow-auto max-h-48">
                  {JSON.stringify(
                    debugData?.[k] ?? { info: state[k]?.details ?? "no-data" },
                    null,
                    2
                  )}
                </pre>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ServicesStatus;
