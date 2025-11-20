const raw = import.meta.env
export const config = {
  NODE_ENV: raw.NODE_ENV ?? 'development',
  API_BASE_URL: String(raw.BACKEND_API_BASE_URL ?? 'http://localhost:8000'),
  timeoutMs: Number(raw.VITE_TIMEOUT_MS ?? 5000),
  featureX: raw.VITE_FEATURE_X === 'true'
} as const
export type Config = typeof config
