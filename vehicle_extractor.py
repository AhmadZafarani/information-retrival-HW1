import re

from parsi_io.parsi_io.modules.address_extractions import AddressExtraction


class VehicleExtractor:
    def __init__(self):
        car_models = r"پراید|پژو|تیبا|دنا|دناپلاس|رانا|بنز|بوگاتی|سمند|رانا|پیکان"
        self.car_models_pattern = re.compile(
            f"با (خودرو|خودروی|ماشین) ({car_models})")

        self.vehicle_names = r"اتوبوس|قطار|خودرو|ماشین|موتور|هواپیما|کشتی|قایق|مینی بوس|تریلی|مترو|تاکسی|هلی کوپتر|بالگرد|دوچرخه|ون|آژانس|موتور سیکلت|فضاپیما"
        self.vehicle_names = f"{self.vehicle_names}|اسب|قاطر|شتر|الاغ|گاری|درشکه|دلیجان|{car_models}"
        self.vehicle_pattern = re.compile(f"با ({self.vehicle_names})")
        self.from_pattern = re.compile(r'از \w+')
        self.to_pattern = re.compile(r'به \w+')

    def __get_car_model_match(self, text: str):
        iterator = list(re.finditer(self.car_models_pattern, text))
        if not iterator:
            return None

        text = iterator[0].group()
        assert text.startswith('با ')

        for c in ['خودرو', 'خودروی', 'ماشین']:
            if text[3:].startswith(f"{c} "):
                return text[4 + len(c):], iterator[0].start() + 4 + len(c), iterator[0].end()
        assert False

    def __get_vehicle_match(self, text: str) -> tuple:
        car_model_match = self.__get_car_model_match(text)
        if car_model_match:
            return car_model_match

        iterator = list(re.finditer(self.vehicle_pattern, text))
        assert len(iterator) == 1
        text = iterator[0].group()
        assert text.startswith('با ')

        return text[3:], iterator[0].start() + 3, iterator[0].end()

    def match_vehicles(self, text: str) -> tuple:
        vehicle, vehicle_start, vehicle_end = self.__get_vehicle_match(text)
        return vehicle, [vehicle_start, vehicle_end]

    def __match_address(self, text: str, pattern: re.Pattern) -> tuple:
        address_ = ""
        address_start = -1
        address_end = -1

        iterator = list(re.finditer(pattern, text))
        assert len(iterator) <= 1

        if iterator:
            m = iterator[0]
            address = AddressExtraction().run(m.group())
            if address['address']:
                assert len(address['address']) == 1
                address_ = address['address'][0]
                address_start = address['address_span'][0] + m.start()
                address_end = address['address_span'][1] + m.start()
        return address_, [address_start, address_end]

    def match_from(self, text: str) -> tuple:
        return self.__match_address(text, self.from_pattern)

    def match_to(self, text: str) -> tuple:
        return self.__match_address(text, self.to_pattern)

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
    input_text = input()
    print(model.run(input_text))
