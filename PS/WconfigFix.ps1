
# �����ܼ�
[string]$configPath = ''
[string]$bakPath = ''
[System.Xml.XmlDocument]$xmlDoc = New-Object System.Xml.XmlDocument
# ���իe�m�@�~
function PrepareTest() {
    #���o���x�W����Web.config
    #-Force :���νT�{������?
    $app = Get-WebApplication -Site 'Default Web Site' -Name 'Caves'
    if (!$app) { throw "$site/$appName not found" }
    $appPath = $app.PhysicalPath 

    #[IO.Path]::Combine($app.PhysicalPath, $folder, 'web.config')
    Write-Host "### �]�w�ɸ��| = $configPath" -ForegroundColor Yellow
    # �ƥ�����
    Copy-Item $appPath "$appPath\web.config" -Force
}
#PrepareTest


function SetConfPath {
    #param (
        #[Parameter(Mandatory = $true)][string]$site, 
        #[Parameter(Mandatory = $true)][string]$appName, 
        #[string]$folder = ''
    #)
    
    $site = 'Default Web Site' 
    $appName = 'Caves' 
    $app = Get-WebApplication -Site $site -Name $appName
    if (!$app) { throw "$site/$appName not found" }
    
    $configPath = [IO.Path]::Combine($app.PhysicalPath, 'web.config')
    Write-Host "### �]�w�ɸ��| = $configPath" -ForegroundColor Yellow
    # �̮ɶ����ͳƥ���Ƨ����| (Get-Location).Path
    $bakPath = Join-Path $app.PhysicalPath ('BAK-' + (Get-Date -Format 'yyyyMMddHHmmss'))
     # �ƥ�����
    [IO.Directory]::CreateDirectory($bakPath) | Out-Null
    if (Test-Path $configPath) {
        Write-Host "�ƥ��ª� $configPath" -ForegroundColor Cyan
        Copy-Item $configPath (Join-Path $bakPath 'web.orig.config')

    }
    else {
        Write-Host "�쥻�L�]�w��" -ForegroundColor Cyan
         '' | Out-File (Join-Path $bakPath 'web.orig.config')
        # ���ͪť� web.config
        @"
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
</configuration>
"@ | Out-File $configPath -Encoding utf8
    }
    
    $xmlDoc.Load($configPath)
    Set-Variable -Name configPath -Value $configPath -Scope 1
    Set-Variable -Name bakPath -Value $bakPath -Scope 1
    #����ק諸log
    Start-Transcript -Path (Join-Path $bakPath "Update.log")
    
}

SetConfPath

function GetXmlNode([string]$xpath, [bool]$autoCreate = $false) {
    $node = $xmlDoc.DocumentElement.SelectSingleNode($xpath) 
    if ($node) { return $node }
    if (!$autoCreate) { return $null }
    $currNode = $xmlDoc.DocumentElement
    $xpath.Split('/') | ForEach-Object {
        $elName = $_
        $m = [System.Text.RegularExpressions.Regex]::Match($elName, "[a-zA-z]+\[@(?<n>.+)=`"(?<v>.+)`"]")
        if ($m.Success) {
            $keyAttrName = $m.Groups['n'].Value
            $keyAttrVal = $m.Groups['v'].Value.Trim("'", "`"")
            $elName = $_.Split('[')[0]
        }
        if (!$currNode.SelectSingleNode($_)) {
            $node = $xmlDoc.CreateElement($elName)    
            if ($keyAttrName) { $node.SetAttribute($keyAttrName, $keyAttrVal) }
            $currNode = $currNode.AppendChild($node) 
        }
        else {
            $currNode = $currNode.SelectSingleNode($_)
        }
    }    
    return $currNode
}
# �b�{�� Attribute �Ȫ��[���e
function AppendXmlElementAttrs([string]$xpath, [Hashtable]$attrs) {
    $node = (GetXmlNode $xpath $true)
    Write-Host "* ���[�ݩ� $xpath" -ForegroundColor Yellow
    $attrs.Keys | ForEach-Object {
        $old = $node.GetAttribute($_)
        $new = $old + [string]$attrs[$_]
        Write-Host "  $old => $new" -ForegroundColor White
        $node.SetAttribute([string]$_, $new)
    }
}
# �s�W XmlElement �ó]�w
function SetXmlElementAttrs([string]$xpath, [Hashtable]$attrs) {
    $node = (GetXmlNode $xpath $true)
    Write-Host "* �]�w�ݩʡG$xpath " -ForegroundColor Yellow
    $attrs.Keys | ForEach-Object {       
        Write-Host "  $_ = $($attrs[$_])" -ForegroundColor White
        $node.SetAttribute([string]$_, [string]$attrs[$_])
    }
}

# �b�{�� Attribute �Ȫ��[���e
AppendXmlElementAttrs 'appSettings/add[@key="ExceptionHandler"]' @{ value = "1120739@taishinbank.com.tw" }
# �s�W XmlElement �ó]�w Attribute ex:system.webServer/httpProtocol/customHeaders/add[@name="X-Frame-Options"]
SetXmlElementAttrs 'appSettings/add[@key="isNewRadar"]' @{ value = 'true' }
# �s�W XmlElement �ó]�w�h�� Attribute
SetXmlElementAttrs 'system.web/httpCookies' @{ requireSSL = 'false'; httpOnlyCookies = 'true' }
#�p�G�S��httpRuntime �o��tag�|���|�ۤw�W�[�H
AppendXmlElementAttrs 'system.web/httpRuntime' @{ targetFramework = '4.8' }


function CommitConfChanges([switch][bool]$force) {
    $newConfPath = Join-Path $bakPath 'web.new.config'
    $origConfPath = Join-Path $bakPath 'web.orig.config'
    $xmlDoc.Save($newConfPath)
    if ($force -or (Read-Host "�T�w�n��s�HY/N") -ieq 'Y') {
        Copy-Item $newConfPath $configPath 
        Write-Host "�w��s $configPath" -ForegroundColor Cyan
        Stop-Transcript
    }
    else {
        Write-Host "���ק�" -ForegroundColor Red
        Stop-Transcript
        . cmd.exe /c "rmdir `"$bakPath`" /s /q"
    }
}

CommitConfChanges