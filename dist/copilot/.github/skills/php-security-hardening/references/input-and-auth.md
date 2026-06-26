# Input Validation, Auth, and Injection Prevention

Validate at boundaries. Authorize in services or policies, not only in controllers.

## Parameterized Query (PDO)

```php
<?php

declare(strict_types=1);

final class UserRepository
{
    public function __construct(private PDO $connection)
    {
    }

    public function findById(string $id): ?array
    {
        $statement = $this->connection->prepare('SELECT id, email FROM users WHERE id = :id');
        $statement->execute(['id' => $id]);

        $row = $statement->fetch(PDO::FETCH_ASSOC);

        return $row === false ? null : $row;
    }
}
```

## Laravel Form Request and Policy

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests;

use App\Models\User;
use Illuminate\Foundation\Http\FormRequest;

final class DeleteUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()?->can('delete', $this->route('user')) ?? false;
    }

    public function rules(): array
    {
        return [];
    }
}
```

```php
<?php

declare(strict_types=1);

namespace App\Policies;

use App\Models\User;

final class UserPolicy
{
    public function delete(User $actor, User $target): bool
    {
        return $actor->isAdmin() || $actor->id === $target->id;
    }
}
```

## Symfony Validator and Voter

```php
<?php

declare(strict_types=1);

namespace App\Dto;

use Symfony\Component\Validator\Constraints as Assert;

final class CreateUserRequest
{
    public function __construct(
        #[Assert\NotBlank]
        #[Assert\Email]
        public string $email,
        #[Assert\NotBlank]
        #[Assert\Length(min: 12)]
        public string $password,
    ) {
    }
}
```

```php
<?php

declare(strict_types=1);

namespace App\Security\Voter;

use Symfony\Component\Security\Core\Authorization\Voter\Voter;

/** @extends Voter<string, mixed> */
final class UserVoter extends Voter
{
    protected function supports(string $attribute, mixed $subject): bool
    {
        return $attribute === 'USER_DELETE';
    }

    protected function voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool
    {
        $user = $token->getUser();
        return $user instanceof AppUser && ($user->isAdmin() || $user->getId() === $subject->getId());
    }
}
```

## Safe File Upload Handling

```php
<?php

declare(strict_types=1);

final class AvatarUploader
{
    private const ALLOWED_MIME = ['image/jpeg', 'image/png'];
    private const MAX_BYTES = 2_000_000;

    public function store(UploadedFile $file): string
    {
        if (!in_array($file->getMimeType(), self::ALLOWED_MIME, true)) {
            throw new InvalidUploadException('Unsupported file type');
        }
        if ($file->getSize() > self::MAX_BYTES) {
            throw new InvalidUploadException('File too large');
        }

        $name = bin2hex(random_bytes(16)) . '.' . $file->guessExtension();
        $file->move($this->storagePath, $name);

        return $name;
    }
}
```

## Output Encoding in Templates

```php
<p><?= htmlspecialchars($user->displayName(), ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?></p>
```

Twig and Blade escape by default — avoid `{!! !!}` or `|raw` unless content is trusted and sanitized.
