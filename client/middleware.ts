import type { NextRequest } from 'next/server';
import { AUTHENTICATION_TOKEN_COOKIE } from './lib/constants';

// TODO: append redirect to URL here
export function middleware(request: NextRequest) {
  const authenticationToken = request.cookies.get(
    AUTHENTICATION_TOKEN_COOKIE
  )?.value;

  if (
    authenticationToken &&
    (request.nextUrl.pathname.startsWith('/login') ||
      request.nextUrl.pathname.startsWith('/register'))
  ) {
    // redirect to dashboard if an authenticated user
    // tries to access the register/ login page
    return Response.redirect(new URL('/', request.url));
  }

  if (
    !authenticationToken &&
    !(
      request.nextUrl.pathname.startsWith('/login') ||
      request.nextUrl.pathname.startsWith('/register')
    )
  ) {
    return Response.redirect(new URL('/login', request.url));
  }
}

export const config = {
  matcher: ['/'],
};
