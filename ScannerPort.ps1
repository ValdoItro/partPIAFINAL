# Escaneo de puertos
# Solicitando direccion IP a escanear:
param([Parameter(Mandatory)] [string]$direccion)
Write-Host($direccion)

# Definimos un array con puertos a escanear y establecemos una variable para Waittime
$portstoscan = @(20,21,22,23,25,50,51,53,80,110,119,135,136,137,138,139,143,161,162,389,443,445,636,902,912,1025,1443,2869,3389,5985,5986,8080,10000)
$waittime = 100

# Generamos bucle foreach para evaluar cada puerto en $portstoscan
foreach ($p in $portstoscan){$TpcObject = New-Object System.Net.Sockets.TcpClient
    try{ $resultado = $TpcObject.ConnectAsync($direccion,$p).Wait($waittime)}catch{}
        if ($resultado -eq "True"){
            Write-Host "Puerto abierto: " -NoNewline; Write-Host $p -ForegroundColor Green
        }
        
    }