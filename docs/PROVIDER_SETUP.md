# Provider Setup Notes

## LinkedIn

The backend uses 3-legged OAuth. Configure Client ID, Client Secret and the exact callback URL in the LinkedIn Developer Portal.

Default callback:

`http://localhost:8000/api/social/linkedin/callback`

The current LinkedIn Posts API uses `/rest/posts` with `Linkedin-Version` and `X-Restli-Protocol-Version: 2.0.0`. The app requests `w_member_social` by default for member posting; the product/permission must be enabled for the LinkedIn app.

## TikTok

The web Login Kit uses the current `/v2/auth/authorize/` flow and token endpoint `/v2/oauth/token/`. Direct posting requires the Content Posting API product and approval for `video.publish` where applicable.

The TikTok redirect URI must satisfy the provider's HTTPS/static redirect rules for web apps.

## Meta / Instagram / Facebook / WhatsApp

Meta integrations are isolated under `app/integrations/social/meta/`. Configure the Graph API version to the version currently enabled/supported by your Meta app. Instagram publishing requires a compatible professional account and the correct Meta permissions. WhatsApp uses its Cloud API business/phone-number configuration rather than the same consumer OAuth pattern.

## X

The X integration uses OAuth 2.0 Authorization Code with PKCE. A durable server-side state/verifier store is recommended for multi-instance production deployments; this code signs the verifier into the short-lived OAuth state token.

## AI

OpenAI and Gemini credentials are optional until AI features are used.

## Payments

Merchant credentials and webhooks are provider-specific. The backend exposes a provider boundary and never treats a frontend payment claim as authoritative.
