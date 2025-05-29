# def init_connectors(connectors: str | list[str] | None = ALL):
#     connector_cfg = get_db_config(database=None)

#     if connectors == ALL:
#         connectors = connector_cfg.keys()
#     elif not isinstance(connectors, list):
#         connectors = [connectors] if connectors else []

#     for key in connectors:
#         try:
#             CONNECTOR_MAP[key](**connector_cfg[key])
#         except KeyError as e:
#             handle_exception(
#                 e,
#                 no_raise=True,
#                 add_pre_message=f"Connector {key} not found in CONNECTOR_MAP",
#             )
#         except Exception as e:
#             handle_exception(
#                 e,
#                 no_raise=True,
#                 add_pre_message=f"Could not instaniate connector {CONNECTOR_MAP[key]} due to:",
#             )
