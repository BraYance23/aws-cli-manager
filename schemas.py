from typing import TypedDict

class DictFormatSGRules(TypedDict):

    list_rows_ingress:list[list[ int | str]]
    dict_rules_egress: dict[ str,dict[ str, str | int | list[ dict[ str,str]]]]
    list_rows_egress:list[list[ int | str]]
    dict_rules_ingress: dict[ str,dict[ str, str | int | list[dict[ str,str]]]]


class DictHeaderRulesSG(TypedDict):
    
    header: list[str]
    title_ingress: str
    title_egress : str