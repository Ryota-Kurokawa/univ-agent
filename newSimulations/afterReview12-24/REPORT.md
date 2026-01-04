# BestPractice SimLoad Extremes

組織全体で負荷がどこに集中しているかを把握しやすいよう、各役職の Top / Average / Min を一覧化し、SimLoad（正規化含む）を比較します。

## 概要テーブル

| Role | Type | Node | SimLoad | Normalized | Score | Tasks | Children |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| CXO | Top | CXO_0 | 47789.11 | 0.449 | 0.31419 | 19622 | 20 |
| CXO | Average | - | 47789.11 | 0.449 | 0.31419 | 19622.00 | 20.00 |
| CXO | Min | CXO_0 | 47789.11 | 0.449 | 0.31419 | 19622 | 20 |
| Director | Top | Director_3 | 78467.50 | 0.736 | 0.51569 | 25053 | 15 |
| Director | Average | - | 70990.10 | 0.666 | 0.46653 | 20305.15 | 11.90 |
| Director | Min | Director_5 | 68415.77 | 0.642 | 0.44960 | 18201 | 11 |
| SeniorManager | Top | SeniorManager_205 | 106551.38 | 1.000 | 0.70019 | 43749 | 15 |
| SeniorManager | Average | - | 94420.38 | 0.886 | 0.62046 | 35405.76 | 12.50 |
| SeniorManager | Min | SeniorManager_203 | 82994.99 | 0.779 | 0.54537 | 26318 | 10 |
| Manager | Top | Manager_2026 | 73838.85 | 0.693 | 0.48522 | 75689 | 10 |
| Manager | Average | - | 64903.34 | 0.609 | 0.42649 | 56624.77 | 7.56 |
| Manager | Min | Manager_1650 | 56872.07 | 0.534 | 0.37370 | 38028 | 5 |
| Player | Top | Player_11337 | 11350.24 | 0.107 | 0.07458 | 6787 | 0 |
| Player | Average | - | 7635.84 | 0.072 | 0.05018 | 6641.70 | 0.00 |
| Player | Min | Player_10950 | 5274.29 | 0.049 | 0.03466 | 6296 | 0 |

### CXO

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | CXO_0 | - | CXO_0 |
| SimLoad | 47789.11 | 47789.11 | 47789.11 |
| Normalized | 0.449 | 0.449 | 0.449 |
| Score | 0.31419 | 0.31419 | 0.31419 |
| Tasks | 19622 | 19622.00 | 19622 |
| Children | 20 | 20.00 | 20 |

### Director

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Director_3 | - | Director_5 |
| SimLoad | 78467.50 | 70990.10 | 68415.77 |
| Normalized | 0.736 | 0.666 | 0.642 |
| Score | 0.51569 | 0.46653 | 0.44960 |
| Tasks | 25053 | 20305.15 | 18201 |
| Children | 15 | 11.90 | 11 |

### SeniorManager

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | SeniorManager_205 | - | SeniorManager_203 |
| SimLoad | 106551.38 | 94420.38 | 82994.99 |
| Normalized | 1.000 | 0.886 | 0.779 |
| Score | 0.70019 | 0.62046 | 0.54537 |
| Tasks | 43749 | 35405.76 | 26318 |
| Children | 15 | 12.50 | 10 |

### Manager

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Manager_2026 | - | Manager_1650 |
| SimLoad | 73838.85 | 64903.34 | 56872.07 |
| Normalized | 0.693 | 0.609 | 0.534 |
| Score | 0.48522 | 0.42649 | 0.37370 |
| Tasks | 75689 | 56624.77 | 38028 |
| Children | 10 | 7.56 | 5 |

### Player

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Player_11337 | - | Player_10950 |
| SimLoad | 11350.24 | 7635.84 | 5274.29 |
| Normalized | 0.107 | 0.072 | 0.049 |
| Score | 0.07458 | 0.05018 | 0.03466 |
| Tasks | 6787 | 6641.70 | 6296 |
| Children | 0 | 0.00 | 0 |
