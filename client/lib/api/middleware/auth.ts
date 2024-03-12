import { Middleware, ResponseContext } from '../../../generated/openapi/v1.0';

export class AuthMiddleware implements Middleware {
  public post(context: ResponseContext): Promise<Response | void> {
    if (context.response.status == 401) {
      // delete auth cookie here
    }
    return Promise.resolve(context.response);
  }
}
