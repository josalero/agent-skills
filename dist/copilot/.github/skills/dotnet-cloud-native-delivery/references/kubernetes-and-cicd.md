# Kubernetes and CI/CD

## Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: orders-api
  template:
    metadata:
      labels:
        app: orders-api
    spec:
      terminationGracePeriodSeconds: 45
      containers:
        - name: api
          image: registry.example.com/orders-api:1.2.3
          ports:
            - containerPort: 8080
          envFrom:
            - secretRef:
                name: orders-api-secrets
            - configMapRef:
                name: orders-api-config
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
```

Set memory limits with headroom above expected GC heap — OOMKill presents as random 502s.

## Secrets in Kubernetes

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: orders-api-secrets
type: Opaque
stringData:
  ConnectionStrings__Default: "Host=postgres;..."
  Auth__SigningKey: "<from-secret-manager>"
```

Prefer External Secrets Operator or cloud secret store sync over committing manifests with values.

## CI/CD Pipeline Stages

```yaml
jobs:
  build:
    steps:
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '9.0.x'
      - run: dotnet restore
      - run: dotnet build --no-restore -c Release
      - run: dotnet test --no-build -c Release
      - run: dotnet publish src/Api/Api.csproj -c Release -o ./publish
      - run: docker build -t registry.example.com/orders-api:${{ github.sha }} .
      - run: docker push registry.example.com/orders-api:${{ github.sha }}
```

Deploy stage:

1. Run EF migrations (job or init container) before switching traffic
2. Apply manifest with immutable tag (`sha`, not `latest`)
3. Wait for rollout and readiness
4. Smoke test critical endpoints

## Observability Hooks

```csharp
builder.Services.AddOpenTelemetry()
    .WithMetrics(metrics => metrics
        .AddAspNetCoreInstrumentation()
        .AddRuntimeInstrumentation()
        .AddPrometheusExporter());
```

Expose `/metrics` when Prometheus scrapes the pod; use structured logging with correlation ids from `Activity.Current`.

## Rollout Checklist

- Database migrations backward-compatible with previous app version during rolling deploy
- Readiness fails when DB unreachable — load balancer stops sending traffic
- Horizontal Pod Autoscaler uses CPU and/or request rate, not memory alone
- Rollback image tag documented in release notes

## Smoke Test After Deploy

```bash
curl -f https://api.example.com/health/ready
curl -f -H "Authorization: Bearer $TOKEN" https://api.example.com/api/v1/orders?page=0&size=1
```

Verify logs show expected OpenTelemetry trace export and no startup configuration binding errors.
