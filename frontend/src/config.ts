// config.ts
const raw = import.meta.env
export const config = {
  NODE_ENV: raw.NODE_ENV ?? 'development',
  API_BASE_URL: String(raw.VITE_API_BASE_URL ?? ''),
  timeoutMs: Number(raw.VITE_TIMEOUT_MS ?? 5000),
  featureX: raw.VITE_FEATURE_X === 'true'
} as const
export type Config = typeof config
