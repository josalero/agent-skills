# Laravel Testing and Queues

Prefer feature tests for HTTP contracts and unit tests for domain rules. Fake external systems at boundaries.

## Feature Test for HTTP Contract

```php
<?php

declare(strict_types=1);

namespace Tests\Feature\Api\V1;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

final class CreateOrderTest extends TestCase
{
    use RefreshDatabase;

    public function testCreatesOrderWithValidPayload(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->postJson('/api/v1/orders', [
            'sku' => 'LEATHER-001',
            'quantity' => 2,
        ]);

        $response
            ->assertCreated()
            ->assertJsonPath('data.sku', 'LEATHER-001')
            ->assertJsonPath('data.status', 'pending');
    }

    public function testRejectsBlankSku(): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)
            ->postJson('/api/v1/orders', ['sku' => '', 'quantity' => 1])
            ->assertUnprocessable()
            ->assertJsonValidationErrors(['sku']);
    }
}
```

## Unit Test for Service Rules

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Services;

use App\Services\PricingService;
use PHPUnit\Framework\TestCase;

final class PricingServiceTest extends TestCase
{
    public function testAppliesDiscountOnce(): void
    {
        $service = new PricingService();

        $first = $service->applyCoupon(100.0, 'SAVE10');
        $second = $service->applyCoupon($first, 'SAVE10');

        self::assertSame(90.0, $first);
        self::assertSame(90.0, $second);
    }
}
```

## Queue Job With Idempotency Guard

```php
<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

final class SendOrderConfirmation implements ShouldQueue
{
    use Dispatchable;
    use InteractsWithQueue;
    use Queueable;
    use SerializesModels;

    public function __construct(public readonly int $orderId)
    {
    }

    public function handle(OrderConfirmationMailer $mailer): void
    {
        $order = Order::query()->findOrFail($this->orderId);

        if ($order->confirmation_sent_at !== null) {
            return;
        }

        $mailer->send($order);
        $order->forceFill(['confirmation_sent_at' => now()])->save();
    }
}
```

## Queue Test With Fake

```php
<?php

declare(strict_types=1);

namespace Tests\Feature\Jobs;

use App\Jobs\SendOrderConfirmation;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

final class SendOrderConfirmationTest extends TestCase
{
    public function testDispatchesJobAfterCheckout(): void
    {
        Queue::fake();

        $this->postJson('/api/v1/checkout', ['orderId' => 42])->assertAccepted();

        Queue::assertPushed(SendOrderConfirmation::class, static fn (SendOrderConfirmation $job): bool => $job->orderId === 42);
    }
}
```

## Verification Commands

```bash
php artisan test --filter=CreateOrderTest
php artisan test tests/Feature/Api/V1
vendor/bin/phpstan analyse app --level=8
```
