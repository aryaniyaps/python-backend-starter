import type { NextRequest } from 'next/server';
import {
  AUTHENTICATION_TOKEN_COOKIE,
  DEFAULT_REDIRECT_TO,
} from './lib/constants';

export function middleware(request: NextRequest) {
  const hasAuthenticationToken = request.cookies.has(
    AUTHENTICATION_TOKEN_COOKIE
  );

  if (
    hasAuthenticationToken &&
    (request.nextUrl.pathname == '/' ||
      request.nextUrl.pathname.startsWith('/login') ||
      request.nextUrl.pathname.startsWith('/register'))
  ) {
    // redirect to dashboard if an authenticated user
    // tries to access the register/ login/ landing page
    return Response.redirect(new URL(DEFAULT_REDIRECT_TO, request.url));
  }

  if (
    !hasAuthenticationToken &&
    !(
      request.nextUrl.pathname.startsWith('/login') ||
      request.nextUrl.pathname.startsWith('/register')
    )
  ) {
    const redirectURL = new URL('/login', request.url);
    redirectURL.searchParams.append('returnTo', request.nextUrl.pathname);
    return Response.redirect(redirectURL);
  }
}

export const config = {
  matcher: ['/', '/dashboard', '/settings/:path*', '/login', '/register'],
};
