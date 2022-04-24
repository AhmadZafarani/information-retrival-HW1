import re

from parsi_io.parsi_io.modules.address_extractions import AddressExtraction


class VehicleExtractor:
    def __init__(self):
        self.vehicle_names = r"اتوبوس|قطار|خودرو|ماشین|موتور|هواپیما|کشتی|قایق|مینی بوس|تریلی|مترو|تاکسی|هلی کوپتر|بالگرد|دوچرخه|ون|آژانس|موتور سیکلت|فضاپیما"
        self.vehicle_names = f"{self.vehicle_names}|اسب|قاطر|شتر|الاغ|گاری|درشکه|دلیجان"
        self.vehicle_names = f"{self.vehicle_names}|پراید|پژو|تیبا|دنا|دناپلاس|رانا|بنز|بوگاتی|سمند|رانا|شاهین|پیکان"
        self.vehicle_pattern = re.compile(f"با ({self.vehicle_names})")
        self.from_pattern = re.compile(r'از \w+')
        self.to_pattern = re.compile(r'به \w+')

    def __get_vehicle_match(self, text: str) -> tuple:
        iterator = list(re.finditer(self.vehicle_pattern, text))
        assert len(iterator) == 1
        text = iterator[0].group()
        assert text.startswith('با ')

        return text[3:], iterator[0].start() + 3, iterator[0].end()

    def match_vehicles(self, text: str) -> tuple:
        vehicle, vehicle_start, vehicle_end = self.__get_vehicle_match(text)
        return vehicle, [vehicle_start, vehicle_end]

    def match_from(self, text: str) -> tuple:
        from_ = ""
        from_start = -1
        from_end = -1

        iterator = list(re.finditer(self.from_pattern, text))
        assert len(iterator) <= 1

        if iterator:
            m = iterator[0]
            address = AddressExtraction().run(m.group())
            if address['address']:
                assert len(address['address']) == 1
                from_ = address['address'][0]
                from_start = address['address_span'][0] + m.start()
                from_end = address['address_span'][1] + m.start()
        return from_, [from_start, from_end]

    def match_to(self, text: str) -> tuple:
        to = ""
        to_start = -1
        to_end = -1

        iterator = list(re.finditer(self.to_pattern, text))
        assert len(iterator) <= 1

        if iterator:
            m = iterator[0]
            address = AddressExtraction().run(m.group())
            if address['address']:
                assert len(address['address']) == 1
                to = address['address'][0]
                to_start = address['address_span'][0] + m.start()
                to_end = address['address_span'][1] + m.start()
        return to, [to_start, to_end]

    def run(self, text: str) -> list:
        # replace half-space with space
        text = text.replace("\u200C", " ")

        vehicle, vehicle_span = self.match_vehicles(text)
        from_, from_span = self.match_from(text)
        to, to_span = self.match_to(text)
        return [
            {
                "from": from_,
                "from_span": from_span,
                "to": to,
                "to_span": to_span,
                "vehicle": vehicle,
                "vehicle_span": vehicle_span,
            },
        ]


if __name__ == '__main__':
    model = VehicleExtractor()
    # input_text = input()
    input_text = 'در حال رانندگی با خودروی تیبا هستم.'
    print(model.run(input_text))
