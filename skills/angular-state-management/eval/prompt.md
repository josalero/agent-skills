# Eval: Angular State Management

## Prompt

Order list state is duplicated in three components with BehaviorSubjects. Cancel on detail page does not refresh list. Recommend and implement smallest fix.

## Expected Agent Behavior

- Centralizes server state in OrderService or store with shared cache
- Uses router/query or refresh/invalidate pattern on mutation
- Avoids introducing NgRx if service + signals/Observable enough
- Tests cancel refresh behavior

## Failure Signals

- window.location.reload
- Global NgRx for one list without repo precedent
- EventEmitter chain through component tree only
