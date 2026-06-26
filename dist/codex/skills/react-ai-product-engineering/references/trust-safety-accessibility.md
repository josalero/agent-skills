# Trust, Safety, and Accessibility

## Markdown Rendering

Sanitize HTML when rendering model markdown.

```tsx
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";

export function AssistantMessage({ content }: { content: string }) {
  return (
    <div className="prose prose-sm max-w-none">
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>
        {content}
      </ReactMarkdown>
    </div>
  );
}
```

Do not render raw HTML from the model without a sanitizer.

## Citations UI

```tsx
{message.sources?.length ? (
  <section aria-label="Sources">
    <h3 className="text-sm font-medium">Sources</h3>
    <ul className="mt-1 space-y-1">
      {message.sources.map((source) => (
        <li key={source.id}>
          {source.href ? (
            <a href={source.href} target="_blank" rel="noreferrer">
              {source.title}
            </a>
          ) : (
            <span>{source.title}</span>
          )}
        </li>
      ))}
    </ul>
  </section>
) : null}
```

## Accessibility for Streaming

```tsx
<div aria-live="polite" aria-busy={status === "streaming"}>
  {text || (status === "streaming" ? "Assistant is responding…" : "")}
</div>
```

- Focus input after send on desktop; preserve mobile keyboard behavior
- Enter to send, Shift+Enter for newline (document in placeholder)
- Visible focus rings on send/stop buttons

## Error Copy (User-Facing)

| Condition | Message |
| --- | --- |
| Timeout | "Response took too long. Try a shorter question or retry." |
| Rate limit | "Too many requests. Wait a moment and try again." |
| Offline | "Connection lost. Check your network and retry." |

Never show stack traces or provider error JSON to users.

## Trust Patterns

- Label as AI-generated content where regulations or UX require it
- Do not imply human support when bot is answering
- Escalation path to human when confidence low or user requests

## Testing

- Component tests for empty, streaming, complete, error states
- Mock stream with async generator in tests
- Optional Playwright smoke for send/receive/cancel happy path
