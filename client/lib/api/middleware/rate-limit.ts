import { Middleware, ResponseContext } from '../../../generated/openapi/v1.0';

export class RateLimitMiddleware implements Middleware {
  public post(context: ResponseContext): Promise<Response | void> {
    if (context.response.status == 429) {
      // show toast about rate limiting here, with retry seconds
    }
    return Promise.resolve(context.response);
  }
}
