import createClient, { Middleware } from 'openapi-fetch';
import type { paths } from '../generated/api/v1';
import { env } from './env';

const errorMiddleware: Middleware = {
  async onResponse(res) {
    if (!res.ok) {
      let body;
      if (res.headers.get('content-type')?.includes('json')) {
        body = await res.clone().json();
      } else {
        body = await res.clone().text();
      }
      throw new Error(body);
    }
    return res;
  },
};

function getBaseUrl(): string {
  if (typeof window !== 'undefined') {
    return env.NEXT_PUBLIC_API_BASE_URL; // browser should use relative url
  }
  return env.API_BASE_URL; // SSR should use localhost
}

export const client = createClient<paths>({
  baseUrl: getBaseUrl(),
  headers: { 'Content-Type': 'application/json' },
  mode: 'cors',
  credentials: 'include',
});

client.use(errorMiddleware);
