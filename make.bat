@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="install-editable" GOTO install-editable
IF "%TARGET%"=="test-run" GOTO test-run


:: INSTALLATION
:: ============
:install-editable
  install\editable-dev
  GOTO end


:: TEST
:: ====
:test-run
  test\run
  GOTO end


:: END
:: ===
:end
