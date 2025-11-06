module.exports = [
"[project]/pages/dashboard.tsx [ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// File: pages/dashboard.tsx
__turbopack_context__.s([
    "getServerSideProps",
    ()=>getServerSideProps
]);
async function getServerSideProps() {
    const FLASK_HEALTH = process.env.FLASK_HEALTH_URL ?? "http://localhost:5060/health";
    const TIMEOUT_MS = 3000;
    const CACHE_TTL_MS = Number(process.env.HEALTH_CACHE_TTL_MS ?? 5000);
    // Simple in-memory cache (persist across requests in dev & prod per process)
    // @ts-ignore - attach cache to global to avoid module-scoped reinitialization in dev HMR
    if (!/*TURBOPACK member replacement*/ __turbopack_context__.g.__FLASK_HEALTH_CACHE) {
        // structure: { value: HealthResult, expiresAt: number }
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        /*TURBOPACK member replacement*/ __turbopack_context__.g.__FLASK_HEALTH_CACHE = {
            value: null,
            expiresAt: 0
        };
    }
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    const cache = /*TURBOPACK member replacement*/ __turbopack_context__.g.__FLASK_HEALTH_CACHE;
    const now = Date.now();
    if (cache.value && cache.expiresAt > now) {
        return {
            props: {
                health: cache.value
            }
        };
    }
    const start = Date.now();
    let health = {
        ok: false,
        statusCode: null,
        body: null,
        latencyMs: null,
        error: undefined,
        checkedAt: new Date().toISOString()
    };
    try {
        const controller = new AbortController();
        const timeout = setTimeout(()=>controller.abort(), TIMEOUT_MS);
        const res = await fetch(FLASK_HEALTH, {
            signal: controller.signal
        });
        clearTimeout(timeout);
        const latencyMs = Date.now() - start;
        let parsedBody = null;
        try {
            parsedBody = await res.json();
        } catch  {
            try {
                parsedBody = await res.text();
            } catch  {
                parsedBody = null;
            }
        }
        health = {
            ok: res.ok,
            statusCode: res.status,
            body: parsedBody,
            latencyMs,
            checkedAt: new Date().toISOString()
        };
    } catch (err) {
        const latencyMs = Date.now() - start;
        health = {
            ok: false,
            statusCode: null,
            body: null,
            latencyMs,
            error: err?.message ?? String(err),
            checkedAt: new Date().toISOString()
        };
    }
    // store in cache
    cache.value = health;
    cache.expiresAt = Date.now() + CACHE_TTL_MS;
    return {
        props: {
            health
        }
    };
}
}),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__2b928e85._.js.map