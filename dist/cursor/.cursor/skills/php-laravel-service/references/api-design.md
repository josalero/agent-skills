# Laravel API Design

Use explicit form requests and API resources rather than exposing Eloquent models directly.

## Controller With Request and Resource Boundaries

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\CreateOrderRequest;
use App\Http\Resources\OrderResource;
use App\Services\OrderService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

final class OrderController extends Controller
{
    public function __construct(private readonly OrderService $orderService)
    {
    }

    public function store(CreateOrderRequest $request): JsonResponse
    {
        $order = $this->orderService->create($request->validated());

        return (new OrderResource($order))
            ->response()
            ->setStatusCode(201);
    }

    public function index(Request $request): AnonymousResourceCollection
    {
        $orders = $this->orderService->paginate(
            page: (int) $request->integer('page', 1),
            perPage: min((int) $request->integer('size', 20), 100),
            status: $request->string('status')->toString() ?: null,
        );

        return OrderResource::collection($orders);
    }
}
```

## Form Request Validation

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

final class CreateOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()?->can('create', Order::class) ?? false;
    }

    /** @return array<string, mixed> */
    public function rules(): array
    {
        return [
            'sku' => ['required', 'string', 'max:64'],
            'quantity' => ['required', 'integer', 'min:1', 'max:1000'],
        ];
    }
}
```

## Stable Error Responses

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Api;

use App\Exceptions\OrderNotFoundException;
use Illuminate\Foundation\Exceptions\Handler;
use Illuminate\Http\JsonResponse;
use Symfony\Component\HttpFoundation\Response;

final class ApiExceptionHandler extends Handler
{
    public function register(): void
    {
        $this->renderable(function (OrderNotFoundException $exception): JsonResponse {
            return response()->json([
                'title' => 'Order Not Found',
                'detail' => 'Order not found',
                'orderId' => $exception->orderId,
            ], Response::HTTP_NOT_FOUND);
        });
    }
}
```

## Service Layer and Transactions

```php
<?php

declare(strict_types=1);

namespace App\Services;

use App\Models\Order;
use Illuminate\Support\Facades\DB;

final class OrderService
{
    /** @param array{sku: string, quantity: int} $payload */
    public function create(array $payload): Order
    {
        return DB::transaction(function () use ($payload): Order {
            return Order::query()->create([
                'sku' => $payload['sku'],
                'quantity' => $payload['quantity'],
                'status' => 'pending',
            ]);
        });
    }
}
```
