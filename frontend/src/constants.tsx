 // src/constants.ts
export const ROUTES = { HOME: '/' } as const
export type RouteKey = keyof typeof ROUTES

export const STATUS_OK = 'OK' as const
export const STATUS_ERROR = 'ERROR' as const
export type StatusType = typeof STATUS_OK | typeof STATUS_ERROR