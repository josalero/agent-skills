# Static Analysis and Coverage

## detekt

```kotlin
detekt {
    buildUponDefaultConfig = true
    config.setFrom(files("$rootDir/detekt.yml"))
}
```

## ktlint

Apply via Gradle plugin with `check` dependency so formatting fails the build.

## JaCoCo Thresholds

```kotlin
tasks.jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit { minimum = "0.80".toBigDecimal() }
        }
    }
}
```

Exclude generated code and DTO packages explicitly — document why.
