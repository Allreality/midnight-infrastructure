module.exports = [
"[externals]/react/jsx-dev-runtime [external] (react/jsx-dev-runtime, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("react/jsx-dev-runtime", () => require("react/jsx-dev-runtime"));

module.exports = mod;
}),
"[project]/pages/dashboard.tsx [ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// File: pages/dashboard.tsx
__turbopack_context__.s([
    "default",
    ()=>Dashboard,
    "getServerSideProps",
    ()=>getServerSideProps
]);
var __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__ = __turbopack_context__.i("[externals]/react/jsx-dev-runtime [external] (react/jsx-dev-runtime, cjs)");
;
function Dashboard({ health }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("main", {
        style: {
            fontFamily: "system-ui, sans-serif",
            padding: 24
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("h1", {
                children: "Dashboard"
            }, void 0, false, {
                fileName: "[project]/pages/dashboard.tsx",
                lineNumber: 20,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("section", {
                style: {
                    marginTop: 20
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("h2", {
                        children: "Flask Health Check"
                    }, void 0, false, {
                        fileName: "[project]/pages/dashboard.tsx",
                        lineNumber: 23,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                        style: {
                            display: "grid",
                            gridTemplateColumns: "140px 1fr",
                            gap: 8,
                            alignItems: "start",
                            maxWidth: 720,
                            background: "#f7f7f8",
                            padding: 12,
                            borderRadius: 8
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("strong", {
                                children: "Status"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 37,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("span", {
                                        style: {
                                            display: "inline-block",
                                            width: 10,
                                            height: 10,
                                            borderRadius: 10,
                                            marginRight: 8,
                                            background: health?.ok ? "#16a34a" : "#dc2626",
                                            verticalAlign: "middle"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/pages/dashboard.tsx",
                                        lineNumber: 39,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("span", {
                                        style: {
                                            fontWeight: 600
                                        },
                                        children: health?.ok ? "Healthy" : "Unhealthy"
                                    }, void 0, false, {
                                        fileName: "[project]/pages/dashboard.tsx",
                                        lineNumber: 50,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 38,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("strong", {
                                children: "HTTP"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 55,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                                children: health?.statusCode ?? "—"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 56,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("strong", {
                                children: "Latency"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 58,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                                children: health?.latencyMs !== null ? `${health.latencyMs} ms` : "—"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 59,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("strong", {
                                children: "Response"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 61,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                                style: {
                                    whiteSpace: "pre-wrap",
                                    fontFamily: "monospace",
                                    fontSize: 13
                                },
                                children: health?.body ? JSON.stringify(health.body, null, 2) : "No body"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 62,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("strong", {
                                children: "Checked At"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 66,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                                children: health?.checkedAt ?? "—"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 67,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("strong", {
                                children: "Error"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 69,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                                style: {
                                    color: "#b91c1c"
                                },
                                children: health?.error ?? "None"
                            }, void 0, false, {
                                fileName: "[project]/pages/dashboard.tsx",
                                lineNumber: 70,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/pages/dashboard.tsx",
                        lineNumber: 25,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/pages/dashboard.tsx",
                lineNumber: 22,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/pages/dashboard.tsx",
        lineNumber: 19,
        columnNumber: 5
    }, this);
}
async function getServerSideProps() {
    const FLASK_HEALTH = process.env.FLASK_HEALTH_URL ?? "http://localhost:5060/health";
    const TIMEOUT_MS = 3000;
    const CACHE_TTL_MS = Number(process.env.HEALTH_CACHE_TTL_MS ?? 5000);
    // Attach a simple in-memory cache to global to survive HMR in dev
    // @ts-ignore
    if (!/*TURBOPACK member replacement*/ __turbopack_context__.g.__FLASK_HEALTH_CACHE) {
        // structure: { value: LocalHealth | null, expiresAt: number }
        // @ts-ignore
        /*TURBOPACK member replacement*/ __turbopack_context__.g.__FLASK_HEALTH_CACHE = {
            value: null,
            expiresAt: 0
        };
    }
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
        error: null,
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

//# sourceMappingURL=%5Broot-of-the-server%5D__a7bb0e5a._.js.map