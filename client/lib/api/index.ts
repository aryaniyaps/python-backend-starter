import {
  AuthenticationApi,
  Configuration,
  UsersApi,
} from '../../generated/openapi/v1.0';

import { env } from '../env';
import { AuthMiddleware } from './middleware/auth';
import { RateLimitMiddleware } from './middleware/rate-limit';

function getBasePath(): string {
  if (typeof window !== 'undefined') {
    return env.NEXT_PUBLIC_API_BASE_URL; // browser should use public URL
  }
  return env.API_BASE_URL; // SSR should use server side URL
}

const configuration = new Configuration({
  basePath: getBasePath(),
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  middleware: [new AuthMiddleware(), new RateLimitMiddleware()],
});

export const usersApi = new UsersApi(configuration);

export const authenticationApi = new AuthenticationApi(configuration);
