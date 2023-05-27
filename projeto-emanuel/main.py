# -- coding: utf-8 --
# Author:Alan Targino
# Data: 27/05/23
# Description: O Código abaixo tem como finalidade fazer requisições a API do Zabbix. Lista todos os hosts e cria um item específico nesse host.

import json # importa o modulo que processa objetos json
import modules.zabbix as zabbix # Import do Módulo Zabbix que está na pasta modules do projeto corrente

# Declaração de variáveis Globais
global USER_ZBX
global PASS_ZBX
global URL_ZBX

# Definição das variáveis
USER_ZBX = "USER AQUI"
PASS_ZBX = "PASS AQUI"
URL_ZBX = "https://zabbix-hubble.connect.dock.tech/api_jsonrpc.php"

def concatena_list_hosts_zabbix(zapi):
    """Retorna uma list com hostid, IP e Hostname. Ex:
    [{"hostid" = "1234", "host" = "abcd", "ip" = 1.1.1.1"}]
    """
    
    # Listar todos os hosts do Zabbix pelo Name
    list_name = zabbix.busca_name_hosts(zapi)
    # Listar todos os hosts do Zabbix pelo IP
    list_ip = zabbix.busca_interfaces_hosts(zapi)
    # Lista concatenada
    list_final = []
    
    for hostname in list_name:
        hostid = hostname['hostid']
        for hostip in list_ip:
            if hostip['hostid'] == hostid:
                new_host = {
                    'hostid': hostid,
                    'host': hostname['host'],
                    'interfaceid': hostip['interfaceid'],
                    'ip': hostip['ip'],
                }
                #Adicona um novo host na lista
                list_final.append(new_host)
                break
    
    return list_final

def percentual_progresso(list, count) -> int:
    """retorna o valor do progresso em inteiro"""
    tamanho_lista = len(list)
    percentual_atual = (count * 100) // tamanho_lista

    # Retorna 100 se for o último loop
    if (tamanho_lista - 1) == count:
        return 100
    else: 
        return percentual_atual

def cria_item_check_latency(zapi, ip, host, item_name):
    hostid = host['hostid']
    interfaceid = host['interfaceid']
    tags = [
        {
            'tag': 'Application',
            'value': 'latency'
        }
    ]
    retorno_api_zabbix = zabbix.create_item(zapi, hostid, interfaceid, item_name, "check-latency["+ip+"]", tags)

    # Verifica se teve erro
    if retorno_api_zabbix[0] == 1:
        print(retorno_api_zabbix[1])
    else:
        print("Item criado com SUCESSO!")

def cria_monitoria(list_hosts, zapi):
    # Percorre cada host da lista
    progresso = 0 # Variável para medir o progresso do for de hosts (contador)
    percent_old = 0 # Variável para salvar o último valor percentual do progresso.
    for host in list_hosts:
        print("Criando item de latência no host: ", host['host'])
        # Obtem o percentual progredido
        percent_now = percentual_progresso(list_hosts, progresso)
        # Só printa se o valor atual for maior que o anterior (Evita duplicidades de percentual)
        if (percent_now > percent_old) or progresso == 0:
            print("-> Progresso: " + str(percent_now) + "%\n")
        
        # Separando os octetos para tratar melhor
        ip_octetos = host['ip'].split(".")

        # Verifica se é um FW Slave comparando o último octeto
        if ip_octetos[3] == "250":
            # Cria o item de latência para checar o Master
            ip_fw_master = ip_octetos[0] + "." + ip_octetos[1] + "." + ip_octetos[2] + ".251" # Definido o IP do FW Master
            cria_item_check_latency(zapi, ip_fw_master, host, "Latência do FW Master")

        # Verifica se é um FW Master comparando o último octeto
        elif ip_octetos[3] == "251":
            # Cria o item de latência para checar o Slave
            ip_fw_slave = ip_octetos[0] + "." + ip_octetos[1] + "." + ip_octetos[2] + ".250" # Definido o IP do FW Slave
            cria_item_check_latency(zapi, ip_fw_slave, host, "Latência do FW Slave")
            
        # Incrementa o loop em +1
        progresso += 1
        # Salva o valor percentual numa variavel
        percent_old = percent_now

def main():
    """Start da Mágica"""
    # Autenticação e retorno do Zapi
    print("Autenticando no Zabbix...")
    zapi = zabbix.autentica(USER_ZBX, PASS_ZBX, URL_ZBX)

    # Lista de Hosts do Zabbix
    print("Consumindo a API do Zabbix para coletar os Hosts configurados...")
    list_concatenada_de_hosts = concatena_list_hosts_zabbix(zapi)

    # Cria a monitoria
    cria_monitoria(list_concatenada_de_hosts, zapi)

# Start da Mágica
main()
