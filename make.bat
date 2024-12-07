@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="install-editable" GOTO install-editable
IF "%TARGET%"=="lint-all" GOTO lint-all
IF "%TARGET%"=="test-all" GOTO test-all


:: INSTALLATION
:: ============
:install-editable
  install\Windows\editable-dev
  GOTO end


:: LINTING
:: =======
:lint-all
  lint\all
  GOTO end


:: TESTING
:: =======
:test-all
  test\all
  GOTO end


:: END
:: ===
:end
