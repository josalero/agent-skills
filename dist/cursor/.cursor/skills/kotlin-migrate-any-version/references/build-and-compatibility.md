# Build and Compatibility

## Gradle Kotlin DSL

```kotlin
plugins {
    kotlin("jvm") version "2.1.0"
}

kotlin {
    jvmToolchain(21)
    compilerOptions {
        freeCompilerArgs.add("-Xjsr305=strict")
    }
}
```

## JVM Target Alignment

Ensure `jvmToolchain`, `kotlinOptions.jvmTarget`, and Java plugin `release` agree.

## Library Alignment

Use BOM imports for kotlinx.coroutines and serialization when possible.

## Verification Commands

```bash
./gradlew clean check
./gradlew dependencies --configuration compileClasspath | grep kotlinx
```
