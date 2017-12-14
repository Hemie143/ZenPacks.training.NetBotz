from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )


class NetBotz(SnmpPlugin):
    relname = 'netBotzTemperatureSensors'
    modname = 'ZenPacks.training.NetBotz.NetBotzTemperatureSensor'

    snmpGetTableMaps = (
        GetTableMap(
            'tempSensorTable', '1.3.6.1.4.1.5528.100.4.1.1.1', {
                '.1': 'tempSensorId',
                '.5': 'tempSensorEncId',
                '.6': 'tempSensorPortId',
                }
            ),
        )

    def process(self, device, results, log):
        temp_sensors = results[1].get('tempSensorTable', {})

        rm = self.relMap()
        for snmpindex, row in temp_sensors.items():
            name = row.get('tempSensorId')
            if not name:
                log.warn('Skipping temperature sensor with no name')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'enclosure': row.get('tempSensorEncId'),
                'port': row.get('tempSensorPortId'),
            }))

        return rm