// File: pages/dashboard.tsx
import React from "react";

type HealthResult = {
  ok: boolean;
  statusCode: number | null;
  body: any | null;
  latencyMs: number | null;
  error?: string | null;
  checkedAt: string;
};

type Props = {
  health: HealthResult;
};

export default function Dashboard({ health }: Props) {
  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: 24 }}>
      <h1>Dashboard</h1>

      <section style={{ marginTop: 20 }}>
        <h2>Flask Health Check</h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "140px 1fr",
            gap: 8,
            alignItems: "start",
            maxWidth: 720,
            background: "#f7f7f8",
            padding: 12,
            borderRadius: 8,
          }}
        >
          <strong>Status</strong>
          <div>
            <span
              style={{
                display: "inline-block",
                width: 10,
                height: 10,
                borderRadius: 10,
                marginRight: 8,
                background: health?.ok ? "#16a34a" : "#dc2626",
                verticalAlign: "middle",
              }}
            />
            <span style={{ fontWeight: 600 }}>
              {health?.ok ? "Healthy" : "Unhealthy"}
            </span>
          </div>

          <strong>HTTP</strong>
          <div>{health?.statusCode ?? "—"}</div>

          <strong>Latency</strong>
          <div>{health?.latencyMs !== null ? `${health.latencyMs} ms` : "—"}</div>

          <strong>Response</strong>
          <div style={{ whiteSpace: "pre-wrap", fontFamily: "monospace", fontSize: 13 }}>
            {health?.body ? JSON.stringify(health.body, null, 2) : "No body"}
          </div>

          <strong>Checked At</strong>
          <div>{health?.checkedAt ?? "—"}</div>

          <strong>Error</strong>
          <div style={{ color: "#b91c1c" }}>{health?.error ?? "None"}</div>
        </div>
      </section>
    </main>
  );
}

export async function getServerSideProps() {
  const FLASK_HEALTH = process.env.FLASK_HEALTH_URL ?? "http://localhost:5060/health";
  const TIMEOUT_MS = 3000;
  const CACHE_TTL_MS = Number(process.env.HEALTH_CACHE_TTL_MS ?? 5000);

  // Simple HealthResult local type (kept here for clarity)
  type LocalHealth = {
    ok: boolean;
    statusCode: number | null;
    body: any | null;
    latencyMs: number | null;
    error?: string | null;
    checkedAt: string;
  };

  // Attach a simple in-memory cache to global to survive HMR in dev
  // @ts-ignore
  if (!global.__FLASK_HEALTH_CACHE) {
    // structure: { value: LocalHealth | null, expiresAt: number }
    // @ts-ignore
    global.__FLASK_HEALTH_CACHE = { value: null, expiresAt: 0 };
  }
  // @ts-ignore
  const cache: { value: LocalHealth | null; expiresAt: number } = global.__FLASK_HEALTH_CACHE;

  const now = Date.now();
  if (cache.value && cache.expiresAt > now) {
    return { props: { health: cache.value } };
  }

  const start = Date.now();
  let health: LocalHealth = {
    ok: false,
    statusCode: null,
    body: null,
    latencyMs: null,
    error: null,
    checkedAt: new Date().toISOString(),
  };

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);

    const res = await fetch(FLASK_HEALTH, { signal: controller.signal });
    clearTimeout(timeout);

    const latencyMs = Date.now() - start;
    let parsedBody: any = null;
    try {
      parsedBody = await res.json();
    } catch {
      try {
        parsedBody = await res.text();
      } catch {
        parsedBody = null;
      }
    }

    health = {
      ok: res.ok,
      statusCode: res.status,
      body: parsedBody,
      latencyMs,
      checkedAt: new Date().toISOString(),
    };
  } catch (err: any) {
    const latencyMs = Date.now() - start;
    health = {
      ok: false,
      statusCode: null,
      body: null,
      latencyMs,
      error: err?.message ?? String(err),
      checkedAt: new Date().toISOString(),
    };
  }

  // store in cache
  cache.value = health;
  cache.expiresAt = Date.now() + CACHE_TTL_MS;

  return { props: { health } };
}