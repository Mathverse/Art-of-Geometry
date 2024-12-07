@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="install-editable" GOTO install-editable
IF "%TARGET%"=="lint-all" GOTO lint-all
IF "%TARGET%"=="test-run" GOTO test-run


:: INSTALLATION
:: ============
:install-editable
  install\editable-dev
  GOTO end


:: LINTING
:: =======
:lint-all
  lint\all
  GOTO end


:: TESTING
:: =======
:test-run
  test\run
  GOTO end


:: END
:: ===
:end
