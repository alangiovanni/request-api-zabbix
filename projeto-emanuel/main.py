# -- coding: utf-8 --
# Author: João Beserra e Alan Targino / joao.beserra@baseservice.io e alan.targino@rpe.tech
# Data: 02/02/23
# Description: O Código abaixo tem como finalidade fazer requisições a API do Zabbix e criar um arquivo em JSON contendo todos os dados encontrados.

import json # importa o modulo que processa objetos json
import modules.zabbix as zabbix # Import do Módulo Zabbix que está na pasta modules do projeto corrente

# Declaração de variáveis Globais
global USER_ZBX
global PASS_ZBX

# Definição das variáveis
USER_ZBX = "USUARIO AQUI"
PASS_ZBX = "SENHA AQUI"

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

def main():
    """Start da Mágica"""
    # Autenticação e retorno do Zapi
    print("Autenticando no Zabbix...")
    zapi = zabbix.autentica(USER_ZBX, PASS_ZBX)

    # Lista de Hosts do Zabbix
    print("Consumindo a API do Zabbix para coletar os Hosts configurados...")
    list_concatenada_de_hosts = concatena_list_hosts_zabbix(zapi)

    # Joga na Tela a lista
    print(list_concatenada_de_hosts)

# Start da Mágica
main()
