# Overlays and Keyboard

## Modal Focus Pattern

```tsx
export function ConfirmDialog({ open, title, onConfirm, onCancel }: ConfirmDialogProps) {
  const cancelRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (open) cancelRef.current?.focus();
  }, [open]);

  if (!open) return null;

  return (
    <div role="presentation" className="fixed inset-0 bg-black/40" onMouseDown={onCancel}>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-title"
        className="mx-auto mt-24 max-w-md rounded bg-white p-6"
        onMouseDown={(e) => e.stopPropagation()}
      >
        <h2 id="confirm-title" className="text-lg font-semibold">
          {title}
        </h2>
        <div className="mt-6 flex justify-end gap-2">
          <button ref={cancelRef} type="button" onClick={onCancel}>
            Cancel
          </button>
          <button type="button" onClick={onConfirm}>
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}
```

Prefer headless library (Radix, React Aria) when project already uses one — do not reinvent focus trap.

## Escape to Close

```tsx
useEffect(() => {
  if (!open) return;
  const onKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Escape") onCancel();
  };
  window.addEventListener("keydown", onKeyDown);
  return () => window.removeEventListener("keydown", onKeyDown);
}, [open, onCancel]);
```

## Live Regions (Use Sparingly)

```tsx
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {statusMessage}
</div>
```

Announce completion/errors — not every character typed.

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Or Tailwind `motion-reduce:` utilities when available.
