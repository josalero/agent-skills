# Symfony Services, Messenger, and Testing

Prefer constructor injection and autowiring. Keep handlers thin and services focused.

## Messenger Handler

```php
<?php

declare(strict_types=1);

namespace App\MessageHandler;

use App\Message\SendOrderConfirmation;
use App\Service\OrderConfirmationMailer;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler]
final class SendOrderConfirmationHandler
{
    public function __construct(private OrderConfirmationMailer $mailer)
    {
    }

    public function __invoke(SendOrderConfirmation $message): void
    {
        $this->mailer->send($message->orderId);
    }
}
```

## Unit Test for Service Rules

```php
<?php

declare(strict_types=1);

namespace App\Tests\Unit\Service;

use App\Service\PricingService;
use PHPUnit\Framework\TestCase;

final class PricingServiceTest extends TestCase
{
    public function testAppliesDiscountOnce(): void
    {
        $service = new PricingService();

        self::assertSame(90.0, $service->applyCoupon(100.0, 'SAVE10'));
        self::assertSame(90.0, $service->applyCoupon(90.0, 'SAVE10'));
    }
}
```

## WebTestCase for HTTP Contract

```php
<?php

declare(strict_types=1);

namespace App\Tests\Controller\Api\V1;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

final class OrderControllerTest extends WebTestCase
{
    public function testCreateOrderRequiresAuthentication(): void
    {
        $client = static::createClient();
        $client->request(
            'POST',
            '/api/v1/orders',
            server: ['CONTENT_TYPE' => 'application/json'],
            content: json_encode(['sku' => 'LEATHER-001', 'quantity' => 2], JSON_THROW_ON_ERROR),
        );

        self::assertResponseStatusCodeSame(401);
    }
}
```

## Kernel Test for Repository Integration

```php
<?php

declare(strict_types=1);

namespace App\Tests\Repository;

use App\Entity\Order;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

final class OrderRepositoryTest extends KernelTestCase
{
    public function testFindsOpenOrders(): void
    {
        self::bootKernel();
        $repository = self::getContainer()->get(OrderRepository::class);

        $count = $repository->count(['status' => 'open']);

        self::assertIsInt($count);
    }
}
```

## Verification Commands

```bash
symfony php bin/phpunit --filter OrderControllerTest
symfony php bin/phpunit tests/Unit
symfony php bin/console lint:container
symfony php bin/console debug:router | grep orders
```
