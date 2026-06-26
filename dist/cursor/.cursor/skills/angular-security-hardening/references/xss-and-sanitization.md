# XSS and Sanitization

## Default Interpolation Is Sanitized

```html
<p>{{ userBio }}</p>
```

Angular escapes HTML in interpolation bindings.

## innerHTML Requires Care

```typescript
// Dangerous if content is user-controlled without policy
<div [innerHTML]="userHtml"></div>
```

Angular sanitizes `[innerHTML]` by default — bypass only with explicit trust:

```typescript
constructor(private sanitizer: DomSanitizer) {}

trustedHtml(content: string): SafeHtml {
  // Only when content source is fully trusted and policy-approved
  return this.sanitizer.bypassSecurityTrustHtml(content);
}
```

Document threat model for every bypassSecurityTrust* usage — review in PR.

## URL Sanitization

```html
<a [href]="userUrl">Link</a>
```

Angular sanitizes URLs and blocks `javascript:` schemes in property binding.

## Content Security Policy

Set at CDN/server:

```text
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'
```

Client cannot replace CSP headers.

## Third-Party Scripts

Load analytics/tags with strict allowlist; prefer tag manager with nonce/hash CSP when required.
