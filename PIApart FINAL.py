#Importacion de modulos
import nmap
import subprocess

#Funciones
def lineas(IP):
    n = []
    f = open('{}.txt'.format(IP), 'r')
    for i in f:
        i = i.strip('\n')
        i = i.replace("Puerto abierto: ","")
        n.append(i)
    n.remove(IP)
    f.close()
    return n
def FindIP(IPList):
    print("Nota: Deberia tener la forma siguiente forma 'X.X.X.1/24'")
    P = str(input("Escribe la puerta de enlace "))
    nm = nmap.PortScanner()
    x = nm.scan(P, arguments="-sP")
    for i in x["scan"]:
        IP = x["scan"][i]["addresses"]["ipv4"]
        try:
            MAC = x["scan"][i]["addresses"]["mac"]
            tmp1 = x["scan"][i]["addresses"]["mac"]
            Estado = "Activo"
            try:
                Marca = x["scan"][i]["vendor"][tmp1]
            except:
                Marca = "No disponible"
        except:
            MAC = "No disponible"
            Estado = "Activo"
            Marca = "No disponible"

        IPList.append(IP)
        print("\nIP: {}\nMAC: {}\nDispositivo: {}\nEstado: {}".format(IP, MAC, Marca, Estado))
    return IPList
def PortScan(IPList):
    print(IPList)
    IP = str(input("Escriba una de las IPs anteriores\npara observar sus puertos abiertos:\n"))
    comandPS = "powershell -ExecutionPolicy ByPass -File ScannerPort.ps1 -direccion " + IP
    try:
        active = subprocess.check_output(comandPS)
        f = open('{}.txt'.format(IP), 'w')
        f.write(active.decode())
        f.close()
        print(active.decode())
    except Exception as error:
        print("Error: ",error)
    puertos = lineas(IP)
    return puertos, IP
def VulnScan(puertos, IP):     #VulnScan tarda 5min aprox segun los puertos a analizar
    print(puertos, IP)         #Buscar una forma de reducir el tiempo y hacerlo ver mas limpio
    puertos = ",".join(map(str,puertos))
    comandoPS = "nmap -p {} --script vuln {}".format(puertos,IP)
    subprocess.run(comandoPS, shell=True)
def Menu():
    IP = 0
    IPList = []
    puertos = []
    Control = True
    while Control == True:
        print("\n=================< MENU >=================")
        print("1) Escaneo de IPs en la red")
        print("2) Escaneo de puertos abiertos")
        print("3) Escaneo de vulnerabilidades en puertos")
        print("4) Salir de la herramienta")
        print("==========================================\n")
        x = int(input("Selecciona la opcion que necesites: "))
        if x == 1:
            print("Opcion ",x ," elegida")
            FindIP(IPList)
            print("Presiona enter para volver al menu")
            input()
        elif x == 2:
            #puertos = PortScan(IPList)  #TEMPORAL TESTEO
            #print(puertos)
            if len(IPList) != 0:
                print("Opcion ",x ," elegida")
                puertos,IP = PortScan(IPList)
                print("Presiona enter para volver al menu")
                input()
            else:
                print("LA LISTA ESTA VACIA\nPresiona enter para volver al menu")
                input()
        elif x == 3:
            print("Opcion ", x, " elegida")
            VulnScan(puertos,IP)
            input()
        elif x == 4:
            print(IPList)
            print("Opcion ",x ," elegida")
            Control = False
            print("Funcion finalizada...")
        else:
            print("OPCION NO VALIDA, INTENTE DENUEVO")

Menu()    #Aun existen detalles a pulir pero ya esta al 75%
          #trata de agregar alguna especificaciones de la profa y reduce el tiempo de ejecucion lo
          #mas que se pueda
          #Agrega una funcion para especificar los puertos a analizar