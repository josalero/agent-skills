# Forms and Semantics

## Reactive Form With Label and Error

```typescript
@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <label for="email">Email</label>
      <input id="email" type="email" formControlName="email" autocomplete="email"
             [attr.aria-invalid]="form.controls.email.invalid && form.controls.email.touched"
             aria-describedby="email-error" />
      @if (form.controls.email.invalid && form.controls.email.touched) {
        <p id="email-error" role="alert">Enter a valid email address</p>
      }
      <button type="submit" [disabled]="form.invalid">Save</button>
    </form>
  `,
})
export class ProfileFormComponent {
  readonly form = new FormGroup({
    email: new FormControl("", { nonNullable: true, validators: [Validators.required, Validators.email] }),
  });
}
```

## Landmarks and Skip Link

```html
<a class="skip-link" href="#main">Skip to main content</a>
<header>...</header>
<nav aria-label="Primary">...</nav>
<main id="main" tabindex="-1">...</main>
```

Focus `#main` programmatically after route navigation when implementing skip-to-content behavior.

## Heading Hierarchy

One `h1` per view; use CSS for visual sizing — do not skip levels for styling alone.

## Button vs Router Link

- `routerLink` for navigation
- `button` for actions on current page (open dialog, submit form)
