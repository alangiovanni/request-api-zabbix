# -- coding: utf-8 --
# Author:
# Data: 
# Description: Métodos para a API do Zabbix

from pyzabbix import ZabbixAPI # Módulo de chamada do Zabbix

def autentica(login:str, password:str, url="https://zabbix-hubble.connect.dock.tech/api_jsonrpc.php") -> str:
    """Autenticação do Zabbix"""
    zapi = ZabbixAPI(url)
    zapi.login(login, password)

    return zapi

def busca_interfaces_hosts(zapi):
    """Antiga função: BuscaHosts"""
    dic_hosts = zapi.hostinterface.get(output=["hostid", "ip"])
    return dic_hosts

def busca_name_hosts(zapi):
    """Antiga função: BuscaName"""
    dic_hosts = zapi.host.get(output=["host", "hostids"])
    return dic_hosts