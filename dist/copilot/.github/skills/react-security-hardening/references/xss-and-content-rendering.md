# XSS and Content Rendering

## Safe Markdown (Example)

```tsx
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";

export function UserComment({ markdown }: { markdown: string }) {
  return (
    <ReactMarkdown rehypePlugins={[rehypeSanitize]}>
      {markdown}
    </ReactMarkdown>
  );
}
```

## Never on Untrusted Input

```tsx
// Unsafe
<div dangerouslySetInnerHTML={{ __html: userBio }} />
```

If HTML is required, sanitize with vetted library server-side or client-side — defense in depth preferred.

## URL Validation for Links

```tsx
function SafeExternalLink({ href, children }: { href: string; children: React.ReactNode }) {
  let url: URL;
  try {
    url = new URL(href);
  } catch {
    return <span>{children}</span>;
  }
  if (!["https:", "http:"].includes(url.protocol)) {
    return <span>{children}</span>;
  }
  return (
    <a href={url.toString()} target="_blank" rel="noopener noreferrer">
      {children}
    </a>
  );
}
```

Block `javascript:` URLs from user-provided hrefs.

## DOM-Based XSS via innerHTML Libraries

Audit rich text editors and chart libraries — keep updated and isolate if possible.

## CSP (Server / CDN)

```text
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self';
```

Client code cannot fully substitute for CSP headers.
