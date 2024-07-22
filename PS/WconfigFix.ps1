
# 全域變數
[string]$configPath = ''
[string]$bakPath = ''
[System.Xml.XmlDocument]$xmlDoc = New-Object System.Xml.XmlDocument
# 測試前置作業
function PrepareTest() {
    #取得站台上面的Web.config
    #-Force :不用確認直接做?
    $app = Get-WebApplication -Site 'Default Web Site' -Name 'Caves'
    if (!$app) { throw "$site/$appName not found" }
    $appPath = $app.PhysicalPath 

    #[IO.Path]::Combine($app.PhysicalPath, $folder, 'web.config')
    Write-Host "### 設定檔路徑 = $configPath" -ForegroundColor Yellow
    # 備份原檔
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
    Write-Host "### 設定檔路徑 = $configPath" -ForegroundColor Yellow
    # 依時間產生備份資料夾路徑 (Get-Location).Path
    $bakPath = Join-Path $app.PhysicalPath ('BAK-' + (Get-Date -Format 'yyyyMMddHHmmss'))
     # 備份原檔
    [IO.Directory]::CreateDirectory($bakPath) | Out-Null
    if (Test-Path $configPath) {
        Write-Host "備份舊版 $configPath" -ForegroundColor Cyan
        Copy-Item $configPath (Join-Path $bakPath 'web.orig.config')

    }
    else {
        Write-Host "原本無設定檔" -ForegroundColor Cyan
         '' | Out-File (Join-Path $bakPath 'web.orig.config')
        # 產生空白 web.config
        @"
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
</configuration>
"@ | Out-File $configPath -Encoding utf8
    }
    
    $xmlDoc.Load($configPath)
    Set-Variable -Name configPath -Value $configPath -Scope 1
    Set-Variable -Name bakPath -Value $bakPath -Scope 1
    #執行修改的log
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
# 在現有 Attribute 值附加內容
function AppendXmlElementAttrs([string]$xpath, [Hashtable]$attrs) {
    $node = (GetXmlNode $xpath $true)
    Write-Host "* 附加屬性 $xpath" -ForegroundColor Yellow
    $attrs.Keys | ForEach-Object {
        $old = $node.GetAttribute($_)
        $new = $old + [string]$attrs[$_]
        Write-Host "  $old => $new" -ForegroundColor White
        $node.SetAttribute([string]$_, $new)
    }
}
# 新增 XmlElement 並設定
function SetXmlElementAttrs([string]$xpath, [Hashtable]$attrs) {
    $node = (GetXmlNode $xpath $true)
    Write-Host "* 設定屬性：$xpath " -ForegroundColor Yellow
    $attrs.Keys | ForEach-Object {       
        Write-Host "  $_ = $($attrs[$_])" -ForegroundColor White
        $node.SetAttribute([string]$_, [string]$attrs[$_])
    }
}

# 在現有 Attribute 值附加內容
AppendXmlElementAttrs 'appSettings/add[@key="ExceptionHandler"]' @{ value = "1120739@taishinbank.com.tw" }
# 新增 XmlElement 並設定 Attribute ex:system.webServer/httpProtocol/customHeaders/add[@name="X-Frame-Options"]
SetXmlElementAttrs 'appSettings/add[@key="isNewRadar"]' @{ value = 'true' }
# 新增 XmlElement 並設定多項 Attribute
SetXmlElementAttrs 'system.web/httpCookies' @{ requireSSL = 'false'; httpOnlyCookies = 'true' }
#如果沒有httpRuntime 這個tag會不會自已增加？
AppendXmlElementAttrs 'system.web/httpRuntime' @{ targetFramework = '4.8' }


function CommitConfChanges([switch][bool]$force) {
    $newConfPath = Join-Path $bakPath 'web.new.config'
    $origConfPath = Join-Path $bakPath 'web.orig.config'
    $xmlDoc.Save($newConfPath)
    if ($force -or (Read-Host "確定要更新？Y/N") -ieq 'Y') {
        Copy-Item $newConfPath $configPath 
        Write-Host "已更新 $configPath" -ForegroundColor Cyan
        Stop-Transcript
    }
    else {
        Write-Host "放棄修改" -ForegroundColor Red
        Stop-Transcript
        . cmd.exe /c "rmdir `"$bakPath`" /s /q"
    }
}

CommitConfChanges