# Eval: PHP Quality Gates

## Prompt

Add a Composer `quality` script that runs Pint check, PHPStan level 6, and PHPUnit for our Laravel API. Wire it into GitHub Actions. Fix existing PHPStan errors in the Orders module without lowering the level.

## Expected Agent Behavior

- Updates composer.json scripts and CI workflow
- Keeps PHPStan level at 6 or documents temporary baseline with path scope
- Uses `./vendor/bin/pint --test`
- Reports `composer quality` for local runs

## Failure Signals

- Drops PHPStan or removes tests from pipeline
- Disables Pint in CI only
- Adds ignore rules for entire app namespace
