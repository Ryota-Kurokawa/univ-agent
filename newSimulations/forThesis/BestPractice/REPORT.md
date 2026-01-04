# BestPractice SimLoad Extremes

組織全体で負荷がどこに集中しているかを把握しやすいよう、各役職の Top / Average / Min を一覧化し、SimLoad（正規化含む）を比較します。

## 概要テーブル

| Role | Type | Node | SimLoad | Normalized | Score | Tasks | Children |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| CXO | Top | CXO_0 | 39578.64 | 0.410 | 0.28717 | 20995 | 15 |
| CXO | Average | - | 39578.64 | 0.410 | 0.28717 | 20995.00 | 15.00 |
| CXO | Min | CXO_0 | 39578.64 | 0.410 | 0.28717 | 20995 | 15 |
| Director | Top | Director_13 | 74711.11 | 0.774 | 0.54193 | 32110 | 14 |
| Director | Average | - | 70731.53 | 0.733 | 0.51306 | 28859.27 | 12.93 |
| Director | Min | Director_3 | 68880.48 | 0.714 | 0.49964 | 28330 | 13 |
| SeniorManager | Top | SeniorManager_84 | 96532.87 | 1.000 | 0.70011 | 50911 | 9 |
| SeniorManager | Average | - | 90789.57 | 0.941 | 0.65846 | 46225.55 | 8.44 |
| SeniorManager | Min | SeniorManager_21 | 84069.20 | 0.871 | 0.60972 | 42394 | 8 |
| Manager | Top | Manager_1109 | 74856.95 | 0.775 | 0.54301 | 119192 | 16 |
| Manager | Average | - | 69421.34 | 0.719 | 0.50358 | 106458.67 | 15.03 |
| Manager | Min | Manager_843 | 63513.55 | 0.658 | 0.46073 | 99271 | 14 |
| Player | Top | Player_15711 | 6863.84 | 0.071 | 0.04978 | 6798 | 0 |
| Player | Average | - | 5182.59 | 0.054 | 0.03759 | 6657.90 | 0.00 |
| Player | Min | Player_7333 | 3972.27 | 0.041 | 0.02882 | 6494 | 0 |

### CXO

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | CXO_0 | - | CXO_0 |
| SimLoad | 39578.64 | 39578.64 | 39578.64 |
| Normalized | 0.410 | 0.410 | 0.410 |
| Score | 0.28717 | 0.28717 | 0.28717 |
| Tasks | 20995 | 20995.00 | 20995 |
| Children | 15 | 15.00 | 15 |

### Director

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Director_13 | - | Director_3 |
| SimLoad | 74711.11 | 70731.53 | 68880.48 |
| Normalized | 0.774 | 0.733 | 0.714 |
| Score | 0.54193 | 0.51306 | 0.49964 |
| Tasks | 32110 | 28859.27 | 28330 |
| Children | 14 | 12.93 | 13 |

### SeniorManager

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | SeniorManager_84 | - | SeniorManager_21 |
| SimLoad | 96532.87 | 90789.57 | 84069.20 |
| Normalized | 1.000 | 0.941 | 0.871 |
| Score | 0.70011 | 0.65846 | 0.60972 |
| Tasks | 50911 | 46225.55 | 42394 |
| Children | 9 | 8.44 | 8 |

### Manager

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Manager_1109 | - | Manager_843 |
| SimLoad | 74856.95 | 69421.34 | 63513.55 |
| Normalized | 0.775 | 0.719 | 0.658 |
| Score | 0.54301 | 0.50358 | 0.46073 |
| Tasks | 119192 | 106458.67 | 99271 |
| Children | 16 | 15.03 | 14 |

### Player

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Player_15711 | - | Player_7333 |
| SimLoad | 6863.84 | 5182.59 | 3972.27 |
| Normalized | 0.071 | 0.054 | 0.041 |
| Score | 0.04978 | 0.03759 | 0.02882 |
| Tasks | 6798 | 6657.90 | 6494 |
| Children | 0 | 0.00 | 0 |
