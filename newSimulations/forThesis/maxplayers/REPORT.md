# BestPractice SimLoad Extremes

組織全体で負荷がどこに集中しているかを把握しやすいよう、各役職の Top / Average / Min を一覧化し、SimLoad（正規化含む）を比較します。

## 概要テーブル

| Role | Type | Node | SimLoad | Normalized | Score | Tasks | Children |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| CXO | Top | CXO_0 | 41959.54 | 0.455 | 0.31835 | 20374 | 15 |
| CXO | Average | - | 41959.54 | 0.455 | 0.31835 | 20374.00 | 15.00 |
| CXO | Min | CXO_0 | 41959.54 | 0.455 | 0.31835 | 20374 | 15 |
| Director | Top | Director_11 | 75996.82 | 0.823 | 0.57650 | 29948 | 18 |
| Director | Average | - | 73296.32 | 0.794 | 0.55601 | 27723.47 | 16.93 |
| Director | Min | Director_6 | 71641.85 | 0.776 | 0.54346 | 26502 | 16 |
| SeniorManager | Top | SeniorManager_250 | 92311.74 | 1.000 | 0.70012 | 38186 | 9 |
| SeniorManager | Average | - | 85610.11 | 0.927 | 0.64929 | 34835.70 | 8.44 |
| SeniorManager | Min | SeniorManager_102 | 77997.00 | 0.845 | 0.59155 | 31008 | 8 |
| Manager | Top | Manager_948 | 74358.13 | 0.806 | 0.56401 | 89953 | 12 |
| Manager | Average | - | 68102.99 | 0.738 | 0.51656 | 79446.86 | 11.02 |
| Manager | Min | Manager_1558 | 61750.49 | 0.669 | 0.46838 | 70786 | 10 |
| Player | Top | Player_25513 | 7647.07 | 0.083 | 0.05800 | 6916 | 0 |
| Player | Average | - | 6150.67 | 0.067 | 0.04665 | 6627.19 | 0.00 |
| Player | Min | Player_23391 | 4686.65 | 0.051 | 0.03555 | 6478 | 0 |

### CXO

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | CXO_0 | - | CXO_0 |
| SimLoad | 41959.54 | 41959.54 | 41959.54 |
| Normalized | 0.455 | 0.455 | 0.455 |
| Score | 0.31835 | 0.31835 | 0.31835 |
| Tasks | 20374 | 20374.00 | 20374 |
| Children | 15 | 15.00 | 15 |

### Director

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Director_11 | - | Director_6 |
| SimLoad | 75996.82 | 73296.32 | 71641.85 |
| Normalized | 0.823 | 0.794 | 0.776 |
| Score | 0.57650 | 0.55601 | 0.54346 |
| Tasks | 29948 | 27723.47 | 26502 |
| Children | 18 | 16.93 | 16 |

### SeniorManager

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | SeniorManager_250 | - | SeniorManager_102 |
| SimLoad | 92311.74 | 85610.11 | 77997.00 |
| Normalized | 1.000 | 0.927 | 0.845 |
| Score | 0.70012 | 0.64929 | 0.59155 |
| Tasks | 38186 | 34835.70 | 31008 |
| Children | 9 | 8.44 | 8 |

### Manager

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Manager_948 | - | Manager_1558 |
| SimLoad | 74358.13 | 68102.99 | 61750.49 |
| Normalized | 0.806 | 0.738 | 0.669 |
| Score | 0.56401 | 0.51656 | 0.46838 |
| Tasks | 89953 | 79446.86 | 70786 |
| Children | 12 | 11.02 | 10 |

### Player

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Player_25513 | - | Player_23391 |
| SimLoad | 7647.07 | 6150.67 | 4686.65 |
| Normalized | 0.083 | 0.067 | 0.051 |
| Score | 0.05800 | 0.04665 | 0.03555 |
| Tasks | 6916 | 6627.19 | 6478 |
| Children | 0 | 0.00 | 0 |
