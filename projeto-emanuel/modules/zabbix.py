# -- coding: utf-8 --
# Author:
# Data: 
# Description: Métodos para a API do Zabbix

from pyzabbix import ZabbixAPI, ZabbixAPIException # Módulo de chamada do Zabbix

def autentica(login:str, password:str, url:str) -> str:
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

def create_item(zapi, host_id, interface_id, item_name, key_name, tags_item, item_type=0, value_type=0, delay_item="1m"):
    try:
        zapi.item.create(
            hostid=host_id,
            interfaceid=interface_id,
            name=item_name,
            key_=key_name,
            type=item_type,
            tags=tags_item,
            value_type=value_type,
            delay=delay_item
        )
    except ZabbixAPIException as e:
        return 1, e
    return 0, "ok"