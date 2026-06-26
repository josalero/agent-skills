# Overlays and CDK

## Material Dialog (When Available)

```typescript
this.dialog.open(ConfirmDialogComponent, {
  ariaLabelledBy: "confirm-title",
  autoFocus: "cancel",
  restoreFocus: true,
});
```

Template:

```html
<h2 id="confirm-title" mat-dialog-title>Delete order?</h2>
<mat-dialog-actions align="end">
  <button mat-button mat-dialog-close>Cancel</button>
  <button mat-button [mat-dialog-close]="true" cdkFocusInitial>Confirm</button>
</mat-dialog-actions>
```

## CDK FocusTrap (Custom Overlay)

```typescript
private focusTrap?: FocusTrap;

open(): void {
  this.focusTrap = this.focusTrapFactory.create(this.overlayRef.nativeElement);
  this.focusTrap.focusInitialElement();
}

close(): void {
  this.focusTrap?.destroy();
}
```

## LiveAnnouncer

```typescript
constructor(private readonly liveAnnouncer: LiveAnnouncer) {}

announceSaved(): void {
  void this.liveAnnouncer.announce("Profile saved");
}
```

Use for async completion — not every keystroke.

## Keyboard Handler Pattern

```typescript
@HostListener("keydown", ["$event"])
onKeydown(event: KeyboardEvent): void {
  if (event.key === "Escape") {
    this.close();
  }
}
```

Ensure focus returns to triggering element after close.
