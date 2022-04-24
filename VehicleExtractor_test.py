import unittest

from vehicle_extractor import VehicleExtractor


class TestSum(unittest.TestCase):
    tester = VehicleExtractor()

    def build_output(self, vehicle: str, vehicle_span: list, from_="", from_span=[-1, -1], to="", to_span=[-1, -1]) -> list:
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

    def test_train_from_to(self):
        self.assertEqual(self.tester.run('من با قطار از اصفهان به تهران می‌روم'), self.build_output(
            'قطار', [6, 10], 'اصفهان', [14, 20], 'تهران', [24, 29]))

    def test_horse_from_to(self):
        self.assertEqual(self.tester.run('من با اسب از اصفهان به تهران می‌روم'), self.build_output(
            'اسب', [6, 9], 'اصفهان', [13, 19], 'تهران', [23, 28]))

    def test_half_space_chopter_from_to(self):
        self.assertEqual(self.tester.run('من با هلی‌کوپتر از یزد به بوشهر رفته‌بودم'), self.build_output(
            'هلی کوپتر', [6, 15], 'یزد', [19, 22], 'بوشهر', [26, 31]))

    def test_pride_only_to(self):
        self.assertEqual(self.tester.run('چون بلیت قطار پر شده بود مجبور شدم با پرایدم به تهران بروم.'), self.build_output(
            'پراید', [38, 43], '', [-1, -1], 'تهران', [48, 53]))

    def test_plane_no_to_and_from(self):
        self.assertEqual(self.tester.run('من و خواهرم تیبا معمولا با هواپیما مسافرت می‌کنیم.'), self.build_output(
            'هواپیما', [27, 34], '', [-1, -1], '', [-1, -1]))

    def test_car_model_tiba_no_to_and_from(self):
        self.assertEqual(self.tester.run('در حال رانندگی با خودروی تیبا هستم.'), self.build_output(
            'تیبا', [25, 29], '', [-1, -1], '', [-1, -1]))
    

if __name__ == '__main__':
    unittest.main()
