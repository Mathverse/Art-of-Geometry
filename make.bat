@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="install-editable" GOTO install-editable


:: INSTALLATION
:: ============
:install-editable
  install\install-editable-dev
  GOTO end


:: END
:: ===
:end
