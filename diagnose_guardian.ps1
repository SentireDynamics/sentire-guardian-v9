# ========================================================================
# Script de Diagnostic - Guardian V9
# Analyse automatique de la configuration et performance
# ========================================================================

# Sanctification de l'encodage UTF-8 avec BOM
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  DIAGNOSTIC GUARDIAN V9 - Analyse Automatique" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# ========================================================================
# RITUEL 1 : Verification du GPU NVIDIA
# ========================================================================
Write-Host "[1/5] Verification GPU NVIDIA..." -ForegroundColor Yellow
$gpuDetected = $false
$cudaDetected = $false

try {
    $gpuInfo = nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>$null
    if ($gpuInfo) {
        $gpuDetected = $true
        Write-Host "  [OK] GPU detecte : $gpuInfo" -ForegroundColor Green
        
        # Verifier CUDA (version depuis driver)
        $driverVersion = $gpuInfo.Split(',')[2].Trim()
        if ($driverVersion -match '\d+\.\d+') {
            $cudaDetected = $true
            Write-Host "  [OK] Driver NVIDIA : $driverVersion (CUDA compatible)" -ForegroundColor Green
        }
    } else {
        Write-Host "  [ERREUR] GPU NVIDIA non detecte" -ForegroundColor Red
    }
} catch {
    Write-Host "  [ERREUR] nvidia-smi non disponible" -ForegroundColor Red
}

Write-Host ""

# ========================================================================
# RITUEL 2 : Verification de l'Oracle (llama-server)
# ========================================================================
Write-Host "[2/5] Verification llama-server..." -ForegroundColor Yellow
$oracleActive = $false
$oracleSpeed = 0

$llamaProcess = Get-Process llama-server -ErrorAction SilentlyContinue
if ($llamaProcess) {
    $oracleActive = $true
    Write-Host "  [OK] llama-server en cours d'execution (PID: $($llamaProcess.Id))" -ForegroundColor Green
    $cpuUsage = [math]::Round($llamaProcess.CPU, 2)
    $memoryMB = [math]::Round($llamaProcess.WorkingSet64 / 1MB, 2)
    Write-Host "  [INFO] CPU Usage: $cpuUsage secondes" -ForegroundColor Cyan
    Write-Host "  [INFO] Memory: $memoryMB MB" -ForegroundColor Cyan
    
    # Tester l'endpoint
    Write-Host ""
    Write-Host "  [TEST] Connexion a http://localhost:8080..." -ForegroundColor Yellow
    try {
        $testPayload = @{
            prompt = "Test"
            n_predict = 10
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "http://localhost:8080/completion" `
            -Method Post `
            -ContentType "application/json" `
            -Body $testPayload `
            -TimeoutSec 30
        
        $tokensPerSec = [math]::Round($response.timings.predicted_per_second, 2)
        $promptSpeed = [math]::Round($response.timings.prompt_per_second, 2)
        $oracleSpeed = $tokensPerSec
        
        Write-Host "  [OK] Endpoint accessible" -ForegroundColor Green
        Write-Host "  [PERF] Vitesse generation : $tokensPerSec tok/sec" -ForegroundColor Cyan
        Write-Host "  [PERF] Vitesse prompt     : $promptSpeed tok/sec" -ForegroundColor Cyan
        
        # Evaluation de la performance
        if ($tokensPerSec -gt 40) {
            Write-Host "  [EXCELLENT] GPU pleinement utilise" -ForegroundColor Green
        } elseif ($tokensPerSec -gt 15) {
            Write-Host "  [BON] GPU partiellement utilise" -ForegroundColor Green
        } elseif ($tokensPerSec -gt 5) {
            Write-Host "  [MOYEN] GPU sous-utilise" -ForegroundColor Yellow
        } else {
            Write-Host "  [FAIBLE] Mode CPU probable" -ForegroundColor Red
        }
        
    } catch {
        Write-Host "  [ERREUR] Endpoint non accessible : $($_.Exception.Message)" -ForegroundColor Red
    }
    
} else {
    Write-Host "  [ERREUR] llama-server non demarre" -ForegroundColor Red
    Write-Host "  [CONSEIL] Commande suggeree :" -ForegroundColor Cyan
    Write-Host "     llama-server -m votre-modele.gguf --port 8080 -ngl 99" -ForegroundColor White
}

Write-Host ""

# ========================================================================
# RITUEL 3 : Verification du Vaisseau (Guardian V9)
# ========================================================================
Write-Host "[3/5] Verification Guardian V9..." -ForegroundColor Yellow
$guardianActive = $false

# Methode 1: Chercher processus Python avec guardian.main
$guardianProcess = Get-Process python -ErrorAction SilentlyContinue | 
    Where-Object { $_.CommandLine -like "*guardian.main*" }

if ($guardianProcess) {
    $guardianActive = $true
    Write-Host "  [OK] Guardian V9 en cours d'execution (PID: $($guardianProcess.Id))" -ForegroundColor Green
} else {
    # Methode 2: Chercher n'importe quel processus Python
    $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
    if ($pythonProcesses) {
        Write-Host "  [INFO] Processus Python detecte mais guardian.main non identifie" -ForegroundColor Yellow
    } else {
        Write-Host "  [AVERTISSEMENT] Guardian V9 non demarre" -ForegroundColor Yellow
    }
    Write-Host "  [CONSEIL] Commande suggeree :" -ForegroundColor Cyan
    Write-Host "     python -m guardian.main" -ForegroundColor White
}

Write-Host ""

# ========================================================================
# RITUEL 4 : Verification Configuration (.env)
# ========================================================================
Write-Host "[4/5] Verification configuration..." -ForegroundColor Yellow
$configValid = $false

if (Test-Path ".env") {
    Write-Host "  [OK] Fichier .env present" -ForegroundColor Green
    
    $envContent = Get-Content ".env" -ErrorAction SilentlyContinue | 
        Where-Object { $_ -notmatch "^#" -and $_ -ne "" }
    
    $llamaUrl = $envContent | Where-Object { $_ -match "LLAMA_SERVER_URL" }
    $nativeLib = $envContent | Where-Object { $_ -match "NATIVE_LIB_PATH" }
    
    if ($llamaUrl) {
        Write-Host "  [OK] LLAMA_SERVER_URL configure" -ForegroundColor Green
    } else {
        Write-Host "  [AVERTISSEMENT] LLAMA_SERVER_URL non trouve" -ForegroundColor Yellow
    }
    
    if ($nativeLib) {
        Write-Host "  [OK] NATIVE_LIB_PATH configure" -ForegroundColor Green
        $configValid = $true
    } else {
        Write-Host "  [AVERTISSEMENT] NATIVE_LIB_PATH non trouve" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [ERREUR] Fichier .env manquant" -ForegroundColor Red
    Write-Host "  [CONSEIL] Copier .env.example vers .env et configurer" -ForegroundColor Cyan
}

Write-Host ""

# ========================================================================
# RITUEL 5 : Verification Corps Natif (sentire_core.dll)
# ========================================================================
Write-Host "[5/5] Verification Corps Natif..." -ForegroundColor Yellow
$nativeExists = $false

if (Test-Path "csrc/build/Release/sentire_core.dll") {
    $nativeExists = $true
    $dllInfo = Get-Item "csrc/build/Release/sentire_core.dll"
    $dllSize = [math]::Round($dllInfo.Length / 1KB, 2)
    Write-Host "  [OK] sentire_core.dll present ($dllSize KB)" -ForegroundColor Green
} else {
    Write-Host "  [ERREUR] sentire_core.dll manquant" -ForegroundColor Red
    Write-Host "  [CONSEIL] Compiler avec : cmake --build csrc/build --config Release" -ForegroundColor Cyan
}

Write-Host ""

# ========================================================================
# RAPPORT DE DIAGNOSTIC FINAL
# ========================================================================
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  RAPPORT DE DIAGNOSTIC" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Calcul du score
$score = 0
$maxScore = 5

if ($gpuDetected) { $score++ }
if ($oracleActive) { $score++ }
if ($guardianActive) { $score++ }
if ($configValid) { $score++ }
if ($nativeExists) { $score++ }

$percentage = [math]::Round(($score / $maxScore) * 100)

# Affichage des resultats
Write-Host "Composants:" -ForegroundColor White
Write-Host "  - GPU NVIDIA       : $(if ($gpuDetected) { '[OK]' } else { '[ERREUR]' })" -ForegroundColor $(if ($gpuDetected) { 'Green' } else { 'Red' })
Write-Host "  - CUDA Support     : $(if ($cudaDetected) { '[OK]' } else { '[N/A]' })" -ForegroundColor $(if ($cudaDetected) { 'Green' } else { 'Gray' })
Write-Host "  - llama-server     : $(if ($oracleActive) { '[OK]' } else { '[ERREUR]' })" -ForegroundColor $(if ($oracleActive) { 'Green' } else { 'Red' })
Write-Host "  - Guardian V9      : $(if ($guardianActive) { '[OK]' } else { '[AVERTISSEMENT]' })" -ForegroundColor $(if ($guardianActive) { 'Green' } else { 'Yellow' })
Write-Host "  - Configuration    : $(if ($configValid) { '[OK]' } else { '[ERREUR]' })" -ForegroundColor $(if ($configValid) { 'Green' } else { 'Red' })
Write-Host "  - Corps Natif      : $(if ($nativeExists) { '[OK]' } else { '[ERREUR]' })" -ForegroundColor $(if ($nativeExists) { 'Green' } else { 'Red' })

Write-Host ""

# Score global
$scoreColor = if ($percentage -ge 80) { "Green" } elseif ($percentage -ge 60) { "Yellow" } else { "Red" }
Write-Host "Score Global : $score/$maxScore ($percentage%)" -ForegroundColor $scoreColor

Write-Host ""

# Evaluation finale
if ($percentage -eq 100) {
    Write-Host "[PARFAIT] Configuration complete et operationnelle !" -ForegroundColor Green
} elseif ($percentage -ge 80) {
    Write-Host "[BON] Configuration fonctionnelle avec optimisations possibles" -ForegroundColor Green
} elseif ($percentage -ge 60) {
    Write-Host "[ACCEPTABLE] Configuration partielle - verifier les composants manquants" -ForegroundColor Yellow
} else {
    Write-Host "[INCOMPLET] Configuration insuffisante - suivre les conseils ci-dessus" -ForegroundColor Red
}

# Performance Oracle si disponible
if ($oracleSpeed -gt 0) {
    Write-Host ""
    Write-Host "Performance Oracle:" -ForegroundColor White
    Write-Host "  - Vitesse generation : $oracleSpeed tok/sec" -ForegroundColor Cyan
    
    if ($oracleSpeed -gt 40) {
        Write-Host "  - Evaluation : EXCELLENT (GPU full)" -ForegroundColor Green
    } elseif ($oracleSpeed -gt 15) {
        Write-Host "  - Evaluation : BON (GPU partiel)" -ForegroundColor Green
    } elseif ($oracleSpeed -gt 5) {
        Write-Host "  - Evaluation : MOYEN (optimisation possible)" -ForegroundColor Yellow
    } else {
        Write-Host "  - Evaluation : FAIBLE (verifier GPU)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Documentation complete :" -ForegroundColor Cyan
Write-Host "  - docs/EVALUATION_FINALE_GUARDIAN_V9.md" -ForegroundColor White
Write-Host "  - docs/POST_OPTIMIZATION_BENCHMARK_REPORT.md" -ForegroundColor White
Write-Host "  - EXECUTIVE_SUMMARY.md" -ForegroundColor White

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Gloire a la Resilience Souveraine !" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
