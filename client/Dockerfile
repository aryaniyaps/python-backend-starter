ARG BASE_IMAGE=node:18-alpine3.17
##### DEPENDENCIES

FROM $BASE_IMAGE AS deps
RUN apk add --no-cache libc6-compat openssl1.1-compat

# Set the working directory in the container
WORKDIR /app

# Install dependencies based on the preferred package manager

COPY package.json package-lock.json* ./

RUN npm ci

##### BUILDER

FROM $BASE_IMAGE AS builder

# Set the working directory in the container
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN SKIP_ENV_VALIDATION=1 npm run build

##### DEVELOPMENT

FROM $BASE_IMAGE AS development

# Set the working directory in the container
WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED 1

# Use the --chown option to set file ownership to nextjs for both COPY commands
COPY --from=deps /app/node_modules ./node_modules
COPY . .

EXPOSE 3000

ENV PORT 3000

CMD ["npm", "run", "dev"]

##### PRODUCTION

FROM $BASE_IMAGE AS production

# Set the working directory in the container
WORKDIR /app

ENV NODE_ENV production

ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/next.config.mjs ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
