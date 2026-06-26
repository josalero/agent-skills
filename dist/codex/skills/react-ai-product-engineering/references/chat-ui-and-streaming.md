# Chat UI and Streaming

## Streaming Hook Pattern (fetch + ReadableStream)

```typescript
export function useChatStream() {
  const [text, setText] = useState("");
  const [status, setStatus] = useState<"idle" | "streaming" | "error" | "done">("idle");
  const abortRef = useRef<AbortController | null>(null);

  const send = useCallback(async (message: string) => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setText("");
    setStatus("streaming");

    const response = await fetch("/api/v1/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
      signal: controller.signal,
    });

    if (!response.ok || !response.body) {
      setStatus("error");
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      setText((prev) => prev + decoder.decode(value, { stream: true }));
    }

    setStatus("done");
  }, []);

  const cancel = useCallback(() => {
    abortRef.current?.abort();
    setStatus("idle");
  }, []);

  return { text, status, send, cancel };
}
```

Adapt for SSE event formats if server emits `data:` frames.

## Message List Component States

```tsx
type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: { id: string; title: string; href?: string }[];
  status?: "streaming" | "complete" | "error";
};
```

Render assistant messages with:

- Partial content while `status === "streaming"`
- Source list below completed answers
- Retry button on `error`

## Avoid UI Anti-Patterns

- Spinner only with no partial text during long streams
- Replacing entire page on each token (use incremental append)
- Auto-scroll that fights user reading earlier content (scroll only if near bottom)

## API Client Boundary

Keep fetch logic in `api/chat.ts` or a hook — presentational components receive props only.

```typescript
export async function postChatStream(
  body: ChatRequest,
  signal: AbortSignal,
): Promise<Response> {
  return fetch("/api/v1/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });
}
```

Bearer tokens from memory/session — never from hardcoded env in client bundle for production secrets.
