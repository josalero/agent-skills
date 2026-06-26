# Eval: PHP Security Hardening

## Prompt

Review and harden this Laravel controller and repository code. Fix authentication, authorization, input validation, and query safety. Add focused tests for the security behavior you enforce.

```php
<?php

class UserController extends Controller
{
    public function show(string $id, UserRepository $repository)
    {
        return $repository->findByNativeQuery("SELECT * FROM users WHERE id = {$id}");
    }

    public function store(Request $request, UserRepository $repository)
    {
        $user = new User();
        $user->email = $request->input('email');
        $user->password = $request->input('password');
        $user->role = $request->input('role', 'user');
        Log::info('Created user', ['email' => $user->email, 'password' => $user->password]);
        return $repository->save($user);
    }

    public function destroy(string $id, UserRepository $repository)
    {
        return $repository->delete($id);
    }
}
```

## Expected Agent Behavior

- Identifies missing authentication on sensitive endpoints and unsafe SQL concatenation
- Replaces raw request input with validated form request and hashes passwords before persistence
- Removes password logging and enforces authorization on delete
- Uses parameterized queries or Eloquent/query builder methods
- Adds tests for forbidden access and SQL injection regression where practical
- Summarizes threats fixed, residual risks, and verification commands

## Failure Signals

- Adds middleware without server-side authorization checks in policies or services
- Logs credentials or tokens after "fixing" the controller
- Uses string formatting for SQL with user input
- Disables CSRF globally without explaining the API auth model
- Returns stack traces or query text in error responses
