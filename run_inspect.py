import os, subprocess, glob

test_file = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\Vw_Transporter_2.0_TDI_CR_Bosch_EDC17CP20-518078 nodpf.bin'
if not os.path.exists(test_file):
    bins = glob.glob(r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\**\*.bin', recursive=True)
    test_file = bins[0] if bins else ''

print('Testing with file:', test_file)

ps_script = r'''
$binDir = 'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\engine\bin'
$dict = @{}
foreach ($f in Get-ChildItem $binDir -Include *.dll,*.exe -Recurse) {
    $b = [System.IO.File]::ReadAllBytes($f.FullName)
    try {
        $a = [System.Reflection.Assembly]::Load($b)
        $dict[$a.GetName().Name] = $a
    } catch {}
}
[System.AppDomain]::CurrentDomain.add_AssemblyResolve({
    param($sender, $args)
    $n = (New-Object System.Reflection.AssemblyName($args.Name)).Name
    if ($dict.ContainsKey($n)) { return $dict[$n] }
    return $null
})
$core = $dict['ECU_tuning_solutions']
$engineType = $core.GetType('159A9CA1')
$inputBytes = [System.IO.File]::ReadAllBytes('__TEST_FILE__')
$analyzeMethod = $engineType.GetMethod('651E5701', [System.Reflection.BindingFlags]'Public,NonPublic,Static')
$model = $analyzeMethod.Invoke($null, [object[]]@('test.bin', [byte[]]$inputBytes))

if ($model -ne $null) {
    Write-Host ('Model Type: ' + $model.GetType().FullName)
    foreach ($p in $model.GetType().GetProperties()) {
        $val = $p.GetValue($model)
        Write-Host ($p.Name + ' = ' + $val)
    }
} else {
    Write-Host 'Model is null'
}
'''.replace('__TEST_FILE__', test_file)

ps_path = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\inspect_model.ps1'
with open(ps_path, 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps_path], capture_output=True, text=True)
print('STDOUT:\n', res.stdout)
print('STDERR:\n', res.stderr)
if os.path.exists(ps_path): os.remove(ps_path)
