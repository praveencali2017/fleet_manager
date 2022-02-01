from enum import Enum
# vehicle_data = vd
# tire_pressure = tp
# battery, fuel and geo = bfg
class ConsumerTopic(Enum):
    VEHICLE_TIRE_PRESSURE_CU = 'vd_tp_create_update'
    VEHICLE_BAT_FUEL_GEO_CU = 'vd_bfg_create_update'
