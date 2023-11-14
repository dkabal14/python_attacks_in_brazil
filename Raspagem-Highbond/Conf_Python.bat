@echo off
set BatchPath=%~dp0
setlocal enabledelayedexpansion

::Checando se o ACL 15 está instalado
:teste

::	goto fim
:checagem
	echo Iniciando a checagem do ACL
	dir "%PROGRAMFILES(X86)%\ACL Software\ACL for Windows 15" >nul
	echo %ERRORLEVEL%
	if "%ERRORLEVEL%"=="0" (
		goto inicio
	) ELSE (
		goto fim
	)

:inicio
	::Copia pyengine se ela não existir no perfil do usuário
	echo Iniciando o processo de configuracao do Python no perfil do usuario
	dir "%USERPROFILE%\.pyengine" >nul
	IF NOT "%ERRORLEVEL%"=="0" (
		ECHO ## Iniciando a cópia dos arquivos do python do ACL ##
		robocopy "%PROGRAMFILES(X86)%\ACL Software\ACL for Windows 15\pyengine" "%USERPROFILE%\.pyengine" /E
	) ELSE (
		ECHO ## pyengine ja existe ##
	)

:configPIP	
	::Copia o módulo PIP se o mesmo não existir
	echo Iniciando o processo de configuracao do PIP na pasta pyengine
	dir "%USERPROFILE%\.pyengine\pip" >nul
	IF NOT "%ERRORLEVEL%"=="0" (
		ECHO ## Iniciando a copia dos arquivos do pip para pyengine ##
		robocopy "%BatchPath%Conf_Python\3rdParty" "%USERPROFILE%\.pyengine" /E
	) ELSE (
		ECHO ## PIP ja existe em pyengine ##
	)
:configScripts
	::Criando a pasta Scripts do Python
	echo Iniciando o processo de configuracao da pasta scripts em pyengine
	dir "%USERPROFILE%\.pyengine\Scripts" >nul
	IF NOT "%ERRORLEVEL%"=="0" (
		ECHO ## Criando a pasta Scripts ##
		md "%USERPROFILE%\.pyengine\Scripts"
	) ELSE (
		ECHO ## Scripts ja existe em pyengine ##
	)
:configPyHome
	::Criando a variavel de ambiente ACLPyHome
	echo Iniciando o processo de configuracao da variavel de ambiente ACLPyHome (Escopo do usuário)
	reg query "HKCU\Environment" /v "ACLPyHome"
	IF NOT "%ERRORLEVEL%"=="0" (
		ECHO ## Criando a variável de ambiente ACLPyHome ##
		reg add "HKCU\Environment" /v "ACLPyHome" /t REG_SZ /d "%USERPROFILE%\.pyengine" /f
	) ELSE (
		ECHO ## Variável ACLPyHome ja existe na HiveKey Current User ##
	)
:configPyScripts
	::Criando a variavel de ambiente ACLPyScripts
	echo Iniciando o processo de configuracao da variavel de ambiente ACLPySripts (Escopo do usuário)
	reg query "HKCU\Environment" /v "ACLPyScripts"
	IF NOT "%ERRORLEVEL%"=="0" (
		ECHO ## Criando a variável de ambiente ACLPyHome ##
		reg add "HKCU\Environment" /v "ACLPyScripts" /t REG_SZ /d "%USERPROFILE%\.pyengine\Scripts" /f
	) ELSE (
		ECHO ## Variável ACLPyScripts ja existe na HiveKey Current User ##
	)

:checkPathHome
	::====================================================
	::Check da variável Path
	echo confguracao da variavel path ACLPyHome
	reg query "HKCU\Environment" /v "Path" | FIND "%ACLPyHome%"
	
	IF NOT "%ERRORLEVEL%"=="0" (
		goto pathConfigHome
	) ELSE (
		goto pathConfigHomeFim
		echo pyHome ja existe
	)
	:pathConfigHome
		for /f "tokens=2*" %%a in ('reg query HKCU\Environment /v Path') do (
			set currPath=%%b
		)
		set newPath=%currPath%;%ACLPyHome%;
		echo "newpath: %newPath%"
		reg add "HKCU\Environment" /v "Path" /d "%newPath%" /f
		set oldPath=%currPath%
		echo "oldPath: %oldPath%"
		reg add "HKCU\Environment" /v "oldPathHome" /d "%oldPath%" /f
	:pathConfigHomeFim

:checkPathScripts
	::====================================================
	::Check da variável Scripts
	reg query "HKCU\Environment" /v "Path" | FIND "%ACLPyScripts%"
	
	IF NOT "%ERRORLEVEL%"=="0" (
		goto pathConfigScripts
	) ELSE (
		goto pathConfigScriptsFim
		echo PyScripts ja existe
	)
	:pathConfigScripts
		for /f "tokens=2*" %%a in ('reg query HKCU\Environment /v Path') do (
			set currPath=%%b
		)
		set newPath=%currPath%;%ACLPyScripts%;
		echo "newpath: %newPath%"
		reg add "HKCU\Environment" /v "Path" /d "%newPath%" /f
		set oldPath=%currPath%
		echo "oldPath: %oldPath%"
		reg add "HKCU\Environment" /v "oldPathScripts" /d "%oldPath%" /f
	:pathConfigScriptsFim

:checkPython
	::Checagem dos módulos do Python
	"%USERPROFILE%\.pyengine\python.exe" "%BatchPath%Conf_Python\Check_PreReq.py"

:startScript
	::Inicia a automação
	"%USERPROFILE%\.pyengine\python.exe" "%BatchPath%Conf_Python\HB-Raspagem-Planos_de_Acao-ptbr-export_excel.py"
:fim
	echo "fim"
	pause