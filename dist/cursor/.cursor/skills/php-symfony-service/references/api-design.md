# Symfony API Design

Use explicit input/output DTOs rather than exposing Doctrine entities from controllers.

## Controller With DTO Boundaries

```php
<?php

declare(strict_types=1);

namespace App\Controller\Api\V1;

use App\Dto\CreateOrderRequest;
use App\Dto\OrderResponse;
use App\Service\OrderService;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\MapRequestPayload;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route('/api/v1/orders')]
final class OrderController
{
    public function __construct(private readonly OrderService $orderService)
    {
    }

    #[Route('', methods: ['POST'])]
    #[IsGranted('ROLE_USER')]
    public function create(#[MapRequestPayload] CreateOrderRequest $request): JsonResponse
    {
        $order = $this->orderService->create($request);

        return new JsonResponse(OrderResponse::fromEntity($order), Response::HTTP_CREATED);
    }
}
```

## Validated Input DTO

```php
<?php

declare(strict_types=1);

namespace App\Dto;

use Symfony\Component\Validator\Constraints as Assert;

final class CreateOrderRequest
{
    public function __construct(
        #[Assert\NotBlank]
        #[Assert\Length(max: 64)]
        public string $sku,
        #[Assert\Positive]
        #[Assert\LessThanOrEqual(1000)]
        public int $quantity,
    ) {
    }
}
```

## Stable Problem Response

```php
<?php

declare(strict_types=1);

namespace App\EventListener;

use App\Exception\OrderNotFoundException;
use Symfony\Component\EventDispatcher\Attribute\AsEventListener;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpKernel\Event\ExceptionEvent;
use Symfony\Component\HttpKernel\KernelEvents;

#[AsEventListener(event: KernelEvents::EXCEPTION)]
final class ApiExceptionListener
{
    public function __invoke(ExceptionEvent $event): void
    {
        $throwable = $event->getThrowable();
        if (!$throwable instanceof OrderNotFoundException) {
            return;
        }

        $event->setResponse(new JsonResponse([
            'title' => 'Order Not Found',
            'detail' => 'Order not found',
            'orderId' => $throwable->orderId,
        ], 404));
    }
}
```

## Service With Transaction Boundary

```php
<?php

declare(strict_types=1);

namespace App\Service;

use App\Entity\Order;
use Doctrine\ORM\EntityManagerInterface;

final class OrderService
{
    public function __construct(private EntityManagerInterface $entityManager)
    {
    }

    public function create(CreateOrderRequest $request): Order
    {
        return $this->entityManager->wrapInTransaction(function () use ($request): Order {
            $order = new Order($request->sku, $request->quantity);
            $this->entityManager->persist($order);

            return $order;
        });
    }
}
```
