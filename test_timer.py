from unittest import TestCase
import itertools, math, sys
from timer import Timer
'''
2**10000
'''
inputs = [
        0, 1, -1, 0.1, math.pi, "1", "a", None, sys.maxsize, 
        sys.maxsize + 1, float('inf'), -1*float('inf'), lambda: 1,
        list(), tuple(), dict()
        ]

PRODUCT = list(itertools.product(inputs, inputs))

class TestParse(TestCase):
    
    def setUp(self):
        self.timer = Timer()

    def test_parse_00(self):
        # NOTE [MINUTE]:0 | [HOUR]:0
        hours, minutes = map(str, PRODUCT[0])
        parsed = self.timer.parse(['-m', minutes, '-o', hours])
        self.assertEqual(parsed.hours, hours)
        self.assertEqual(parsed.minutes, minutes)

class TestTotalSeconds(TestCase):

    def setUp(self):
        self.timer = Timer()

    def overflow(self, n):
        ''' A helper for eliminating redundant code '''
        with self.assertRaises(OverflowError) as test:
            self.timer.total_seconds(*PRODUCT[n])
            self.assertEqual(test.exception.message, 
                    "Input cannot be infinity.")

    def zero_value(self, n):
        ''' A helper for eliminating redundant code '''
        with self.assertRaises(ValueError) as test:
            self.timer.total_seconds(*PRODUCT[n])
            self.assertEqual(test.exception.message,
                    "Calculated zero total seconds.")

    def alpha_value(self, n):
        ''' A helper for eliminating redundant code '''
        with self.assertRaises(ValueError) as test:
            self.timer.total_seconds(*PRODUCT[n])
            self.assertEqual(test.exception.message,
                    "Input cannot be a letter.")

    # ---------------------------- #
    # No. |         INPUT          #
    # ---------------------------- #

    # 000   -> [MINUTE]:0 | [HOUR]:0
    def test_total_seconds_000(self): self.zero_value(0)

    # 001   -> [MINUTE]:0 | [HOUR]:1
    def test_total_seconds_001(self):
        self.assertEqual(self.timer.total_seconds(*PRODUCT[1]), 3600)
 
    # 002   -> [MINUTE]:0 | [HOUR]:-1
    def test_total_seconds_002(self):
        self.assertRaises(TypeError, self.timer.total_seconds(*PRODUCT[2]))

    # 003   -> [MINUTE]:0 | [HOUR]:0.1
    def test_total_seconds_003(self):
        self.assertEqual(self.timer.total_seconds(*PRODUCT[3]), 360)

    # 004   -> [MINUTE]:0 | [HOUR]:pi
    def test_total_seconds_004(self):
        self.assertEqual(self.timer.total_seconds(*PRODUCT[4]), 11309)

    # 005   -> [MINUTE]:0 | [HOUR]:'1'
    def test_total_seconds_005(self):
        self.assertEqual(self.timer.total_seconds(*PRODUCT[5]), 3600)

    # 006   -> [MINUTE]:0 | [HOUR]:'a'
    def test_total_seconds_006(self): self.alpha_value(6)
        
    # 007   -> [MINUTE]:0 | [HOUR]:None
    def test_total_seconds_007(self): self.zero_value(7)

    # TODO
    # 008
    # 009

    # 010   -> [MINUTE]:0 | [HOUR]:inf
    def test_total_seconds_010(self): self.overflow(10)
        
    # 011   -> [MINUTE]:0 | [HOUR]:-inf
    def test_total_seconds_11(self): self.overflow(11)

    # TODO
    # 012
    # 013
    # 014
    # 015

    # 016   -> [MINUTE]:1 | [HOUR]:0
    def test_total_seconds_16(self):
        self.assertEqual(self.timer.total_seconds(*PRODUCT[16]), 60)

    # 017   -> [MINUTE]:1 | [HOUR]:1
    def test_total_seconds_17(self):
        self.assertEqual(self.timer.total_seconds(*PRODUCT[17]), 3660)

    # TODO
    # 018
    # 019
    # 020
    # 021
    # 022

    # 023   -> [MINUTE]:1 | [HOUR]:None
    def test_total_seconds_23(self):
        self.assertEqual(self.timer.total_seconds(*PRODUCT[23]), 60)

    # TODO
    # 024
    # 025

    # 026   -> [MINUTE]:1 | [HOUR]:inf
    def test_total_seconds_26(self): self.overflow(26)

    # 027   -> [MINUTE]:1 | [HOUR]:-inf
    def test_total_seconds_27(self): self.overflow(27)

    # TODO
    # 028
    # 029
    # 030
    # 031
    # 032
    # 033
    # 034
    # 035
    # 036
    # 037
    # 038
    # 039
    # 040
    # 041
    # 042
    # 043
    # 044
    # 045
    # 046
    # 047
    # 048
    # 049
    # 050
    # 051
    # 052
    # 053
    # 054
    # 055
    # 056
    # 057
    # 058
    # 059
    # 060
    # 061
    # 062
    # 063
    # 064
    # 065
    # 066
    # 067
    # 068
    # 069
    # 070
    # 071
    # 072
    # 073
    # 074
    # 075
    # 076
    # 077
    # 078
    # 079
    # 080
    # 081
    # 082
    # 083
    # 084
    # 085
    # 086
    # 087
    # 088
    # 089
    # 090
    # 091
    # 092
    # 093
    # 094
    # 095
    # 096
    # 097
    # 098
    # 099
    # 100
    # 101
    # 102
    # 103
    # 104
    # 105
    # 106
    # 107
    # 108
    # 109
    # 110
    # 111

    # 112   -> [MINUTE]:None | [HOUR]:0
    def test_total_seconds_112(self): self.zero_value(112)

    # 113   -> [MINUTE]:None | [HOUR]:1
    def test_total_seconds_113(self):
        self.assertEqual(self.timer.total_seconds(*PRODUCT[113]), 3600)

    # TODO
    # 114
    # 115
    # 116
    # 117
    # 118

    # 119   -> [MINUTE]:None | [HOUR]:None
    def test_total_seconds_119(self): self.zero_value(119)
 
    # TODO
    # 120
    # 121

    # 122   -> [MINUTE]:None | [HOUR]:inf
    def test_total_seconds_122(self): self.overflow(122)

    # 123   -> [MINUTE]:None | [HOUR]:-inf
    def test_total_seconds_123(self): self.overflow(123)

    # TODO
    # 124
    # 125
    # 126
    # 127
    # 128
    # 129
    # 130
    # 131
    # 132
    # 133
    # 134
    # 135
    # 136
    # 137
    # 138
    # 139
    # 140
    # 141
    # 142
    # 143
    # 144
    # 145
    # 146
    # 147
    # 148
    # 149
    # 150
    # 151
    # 152
    # 153
    # 154
    # 155
    # 156
    # 157
    # 158
    # 159

    # 160   -> [MINUTE]:inf | [HOUR]:0
    def test_total_seconds_160(self): self.overflow(160)
 
    # 161   -> [MINUTE]:inf | [HOUR]:1
    def test_total_seconds_161(self): self.overflow(161)

    # TODO
    # 162
    # 163
    # 164
    # 165
    # 166

    # 167   -> [MINUTE]:inf | [HOUR]:None
    def test_total_seconds_167(self): self.overflow(167)

    # TODO
    # 168
    # 169
    
    # 170   -> [MINUTE]:inf | [HOUR]:inf
    def test_total_seconds_170(self): self.overflow(170)

    # 171   -> [MINUTE]:inf | [HOUR]:-inf
    def test_total_seconds_171(self): self.overflow(171)

    # TODO
    # 172
    # 173
    # 174
    # 175

    # 176   -> [MINUTE]:-inf | [HOUR]:0
    def test_total_seconds_176(self): self.overflow(176)

    # 177   -> [MINUTE]:-inf | [HOUR]:1
    def test_total_seconds_177(self): self.overflow(177)

    # TODO
    # 178
    # 179
    # 180
    # 181
    # 182

    # 183   -> [MINUTE]:-inf | [HOUR]:None
    def test_total_seconds_183(self): self.overflow(183)

    #TODO
    # 184
    # 185

    # 186   -> [MINUTE]:-inf | [HOUR]:inf
    def test_total_seconds_186(self): self.overflow(186)

    # 187   -> [MINUTE]:-inf | [HOUR]:-inf
    def test_total_seconds_187(self): self.overflow(187)

    #TODO
    # 255

    #def test_schedule(self): pass

if __name__ == '__main__':
    for e, value in enumerate(PRODUCT):
        print(f'{e:0>3}. {value}')
